#!/usr/bin/python3
"""Publish verified Linux artifacts; keep shared configuration/data and code rollback."""

import argparse
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import tarfile
import time
import urllib.request
import uuid

BASE = Path('/var/www/kenfinly-2-deploy')
RELEASES = BASE / 'releases'
SHARED = BASE / 'shared'
INCOMING = Path('/var/lib/kenfinly-deploy/incoming')
PHP = '/usr/bin/php8.4'
MYSQL_CONFIG = '/etc/kenfinly/mysql-app.cnf'
APPROVAL = Path('/etc/kenfinly/approved-migrations.json')
ORIGIN = 'https://my.kenfinly.com'


def run(arguments, cwd=None, capture=False):
    return subprocess.run([str(item) for item in arguments], cwd=cwd, check=True,
                          text=True, stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE if capture else None).stdout


def checksum(path):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def migrations():
    result = subprocess.run(['/usr/bin/mysql', '--defaults-file=' + MYSQL_CONFIG,
                             '--batch', '--skip-column-names', '-e',
                             'SELECT migration FROM migrations ORDER BY migration'],
                            text=True, capture_output=True)
    if result.returncode:
        if '1146' in result.stderr:
            return []
        raise RuntimeError('Cannot inspect the owned application database; publication refused')
    return result.stdout.splitlines()


def schema_fingerprint():
    return hashlib.sha256(json.dumps(migrations()).encode()).hexdigest()


def owned_release(name):
    link = BASE / name
    if not link.is_symlink():
        if link.exists():
            raise RuntimeError('Unexpected non-symlink preserved: ' + str(link))
        return None
    path = link.resolve(strict=True)
    if path.parent != RELEASES.resolve() or not (path / 'DEPLOYMENT.json').is_file():
        raise RuntimeError('Release pointer ownership check failed')
    return path


def switch(name, target):
    temporary = BASE / ('.' + name + '-' + uuid.uuid4().hex)
    temporary.symlink_to(target.relative_to(BASE))
    temporary.replace(BASE / name)


def services():
    active = subprocess.run(['/usr/bin/systemctl', 'is-active', '--quiet', 'kenfinly-fpm.service']).returncode == 0
    run(['/usr/bin/sudo', '-n', '/usr/bin/systemctl', 'reload' if active else 'start', 'kenfinly-fpm.service'])
    # SIGTERM is handled by Laravel; the owned unit allows 300 seconds to finish work.
    run(['/usr/bin/sudo', '-n', '/usr/bin/systemctl', 'restart', 'kenfinly-queue.service'])
    run(['/usr/bin/sudo', '-n', '/usr/bin/systemctl', 'start', 'kenfinly-scheduler.timer'])


def health():
    for attempt in range(20):
        try:
            for path in ['/up', '/login']:
                request = urllib.request.Request(ORIGIN + path, headers={'User-Agent': 'Kenfinly-deploy-health'})
                with urllib.request.urlopen(request, timeout=10) as response:
                    if response.status != 200:
                        raise RuntimeError('Health status is not 200')
            return
        except Exception:
            if attempt == 19:
                raise RuntimeError('Public HTTPS health checks failed; see owned service logs')
            time.sleep(1)


def backup_database(release_id):
    directory = SHARED / 'backups'
    directory.mkdir(mode=0o700, exist_ok=True)
    destination = directory / (release_id + '-before-migrate.sql')
    with destination.open('x') as output:
        subprocess.run(['/usr/bin/mysqldump', '--defaults-file=' + MYSQL_CONFIG,
                        '--single-transaction', '--no-tablespaces', '--routines=false', '--triggers',
                        'kenfinly2'], stdout=output, check=True)
    destination.chmod(0o600)


def cache_release(release, refresh_config=False):
    if refresh_config:
        run([PHP, release / 'artisan', 'config:clear', '--no-interaction'], cwd=release)
    for command in ['config:cache', 'event:cache', 'route:cache', 'view:cache']:
        run([PHP, release / 'artisan', command, '--no-interaction'], cwd=release)


def deploy(artifact, sha, build_number, apply_migrations):
    if not re.fullmatch(r'[0-9a-f]{40}', sha) or not re.fullmatch(r'[0-9]+', build_number):
        raise RuntimeError('Invalid commit/build identifier')
    artifact = Path(artifact).resolve(strict=True)
    if artifact.parent != INCOMING.resolve() or artifact.name != sha + '-' + build_number + '.tar.gz':
        raise RuntimeError('Only the exact owned incoming artifact is accepted')
    previous = owned_release('current')
    if previous and not json.loads((previous / 'DEPLOYMENT.json').read_text()).get('health_verified'):
        previous = None
    now = datetime.datetime.now(datetime.timezone.utc)
    release_id = now.strftime('%Y%m%dT%H%M%S%fZ') + '-' + sha[:12] + '-' + build_number
    release = RELEASES / release_id
    release.mkdir(mode=0o755)
    with tarfile.open(artifact, 'r:gz') as archive:
        for member in archive.getmembers():
            parts = Path(member.name).parts
            if member.name.startswith('/') or '..' in parts or '.env' in parts or member.name.strip('./') == 'public/hot':
                raise RuntimeError('Artifact contains forbidden paths; extraction refused')
        archive.extractall(release, filter='data')
    metadata = json.loads((release / 'KENFINLY_BUILD.json').read_text())
    if metadata['source_sha'] != sha or metadata['branch'] != 'develop' or metadata['platform'] != 'Linux/x86_64':
        raise RuntimeError('Artifact identity/platform mismatch')
    if set(metadata['locks']) != {'composer.lock', 'package-lock.json'}:
        raise RuntimeError('Both lockfile identities are required')
    for name, expected in metadata['locks'].items():
        if name not in ['composer.lock', 'package-lock.json'] or checksum(release / name) != expected:
            raise RuntimeError('Lockfile checksum mismatch')
    if (release / 'BUILD_REF').read_text().strip() != sha:
        raise RuntimeError('Build reference mismatch')
    for directory, directories, files in os.walk(release):
        Path(directory).chmod(0o755)
        for filename in files:
            path = Path(directory) / filename
            if not path.is_symlink():
                path.chmod(0o755 if os.access(path, os.X_OK) else 0o644)
    storage = release / 'storage'
    if storage.is_symlink():
        raise RuntimeError('Unexpected source storage symlink')
    if storage.exists():
        if any(path.is_file() and path.name != '.gitignore' for path in storage.rglob('*')):
            raise RuntimeError('Source artifact unexpectedly contains runtime storage data')
        shutil.rmtree(storage)
    storage.symlink_to(SHARED / 'storage')
    (release / '.env').symlink_to(SHARED / '.env')
    (release / 'bootstrap/cache').chmod(0o2770)
    public_storage = release / 'public/storage'
    if public_storage.exists() or public_storage.is_symlink():
        raise RuntimeError('Unexpected public storage path in source artifact')
    public_storage.symlink_to(SHARED / 'storage/app/public')

    run([PHP, release / 'artisan', 'package:discover', '--no-interaction'], cwd=release)
    already = set(migrations())
    pending = [path for path in (release / 'database/migrations').glob('*.php') if path.stem not in already]
    if pending:
        if not apply_migrations:
            raise RuntimeError('Pending migrations require explicit approval and --apply-migrations')
        approval = json.loads(APPROVAL.read_text())
        schema_files = list((release / 'database/migrations').glob('*.php')) + list((release / 'database/schema').glob('*.sql'))
        for path in schema_files:
            if approval.get(str(path.relative_to(release))) != checksum(path):
                raise RuntimeError('Unreviewed migration/schema file: ' + str(path.relative_to(release)))
        backup_database(release_id)
        run([PHP, release / 'artisan', 'down', '--retry=60', '--no-interaction'], cwd=release)
        run([PHP, release / 'artisan', 'migrate', '--force', '--no-interaction'], cwd=release)
    cache_release(release)
    result = {**metadata, 'release_id': release_id, 'artifact_sha256': checksum(artifact),
              'schema_fingerprint': schema_fingerprint(), 'deployed_at': now.isoformat(), 'health_verified': False}
    (release / 'DEPLOYMENT.json').write_text(json.dumps(result, indent=2) + '\n')
    (release / 'DEPLOYMENT.json').chmod(0o640)
    if previous:
        switch('previous', previous)
    switch('current', release)
    try:
        services()
        run([PHP, release / 'artisan', 'queue:restart', '--no-interaction'], cwd=release)
        run([PHP, release / 'artisan', 'up', '--no-interaction'], cwd=release)
        health()
    except Exception:
        if previous and json.loads((previous / 'DEPLOYMENT.json').read_text())['schema_fingerprint'] == schema_fingerprint():
            switch('current', previous)
            services()
            health()
            print('Previous compatible code restored; no database restore was performed.')
        else:
            print('Automatic code restore refused: no compatible previous release; operator review required.')
        raise
    result['health_verified'] = True
    (release / 'DEPLOYMENT.json').write_text(json.dumps(result, indent=2) + '\n')
    (release / 'DEPLOYMENT.json').chmod(0o640)
    print(json.dumps(result, indent=2))


def rollback():
    current, previous = owned_release('current'), owned_release('previous')
    if not current or not previous:
        raise RuntimeError('No verified previous release is available')
    metadata = json.loads((previous / 'DEPLOYMENT.json').read_text())
    if not metadata.get('health_verified'):
        raise RuntimeError('Previous release did not complete health verification')
    if metadata['schema_fingerprint'] != schema_fingerprint():
        raise RuntimeError('Schema differs from the previous release; rollback needs a compatibility review, never a database rewind')
    cache_release(previous, refresh_config=True)
    switch('current', previous)
    try:
        services()
        health()
    except Exception:
        switch('current', current)
        services()
        raise
    switch('previous', current)
    print(json.dumps({'code_rollback': 'passed', 'active': metadata, 'database_restored': False}, indent=2))


def main():
    if pwd.getpwuid(os.geteuid()).pw_name != 'kenfinly-deploy':
        raise RuntimeError('Run only as the dedicated deployment account; never as root')
    os.umask(0o007)
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    publish = commands.add_parser('deploy')
    publish.add_argument('artifact')
    publish.add_argument('sha')
    publish.add_argument('build_number')
    publish.add_argument('--apply-migrations', action='store_true')
    commands.add_parser('rollback')
    commands.add_parser('status')
    arguments = parser.parse_args()
    with (BASE / '.deploy.lock').open('a') as lock:
        os.fchmod(lock.fileno(), 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if arguments.command == 'deploy':
            deploy(arguments.artifact, arguments.sha, arguments.build_number, arguments.apply_migrations)
        elif arguments.command == 'rollback':
            rollback()
        else:
            current = owned_release('current')
            if not current:
                raise RuntimeError('No active release')
            print((current / 'DEPLOYMENT.json').read_text())


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('DEPLOYMENT FAILED: ' + str(error), file=__import__('sys').stderr)
        raise SystemExit(1)
