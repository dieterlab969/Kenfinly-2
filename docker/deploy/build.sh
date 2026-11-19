#!/bin/bash
# Runs on the Ubuntu Jenkins executor. No production configuration is loaded here.
set -euo pipefail
set +x
umask 0077

source_dir=${1:?Usage: build.sh SOURCE_DIR EXPECTED_SHA BUILD_NUMBER}
expected_sha=${2:?Missing exact commit}
build_number=${3:?Missing build number}
[[ "$expected_sha" =~ ^[0-9a-f]{40}$ ]] || { echo 'Invalid commit SHA' >&2; exit 2; }
[[ "$build_number" =~ ^[0-9]+$ ]] || { echo 'Invalid build number' >&2; exit 2; }
[[ $(uname -s) = Linux && $(uname -m) = x86_64 ]] || { echo 'Build on the reviewed Linux x86_64 executor' >&2; exit 2; }
export PATH=/opt/kenfinly-tools/bin:/opt/kenfinly-tools/node/bin:/usr/bin:/bin
php -r 'exit(PHP_MAJOR_VERSION === 8 && PHP_MINOR_VERSION === 4 ? 0 : 1);'
node -e 'if (!process.version.startsWith("v24.")) process.exit(1)'
cd "$source_dir"
[[ $(git rev-parse HEAD) = "$expected_sha" ]] || { echo 'Checkout differs from selected commit' >&2; exit 2; }
[[ $(git remote get-url origin) = git@github.com:dieterlab969/Kenfinly-2.git ]] || { echo 'Unexpected source repository' >&2; exit 2; }
[[ $(git config --get-all remote.origin.fetch) = +refs/heads/deploy/my-kenfinly:refs/remotes/origin/deploy/my-kenfinly ]] || { echo 'Only the deployment branch may be fetched' >&2; exit 2; }
[[ $(git rev-parse refs/remotes/origin/deploy/my-kenfinly) = "$expected_sha" ]] || { echo 'Selected commit is not the fetched deployment head' >&2; exit 2; }
[[ ! -e .env && ! -L .env ]] || { echo 'Unexpected workspace .env preserved; inspect before building' >&2; exit 2; }
[[ -f ${CI_ENV_FILE:?Jenkins secret-file credential is required} ]] || exit 2
set -a
. "$CI_ENV_FILE"
set +a
[[ "$APP_ENV" = testing && "$DB_HOST" = 127.0.0.1 && "$DB_PORT" = 13316 && "$DB_DATABASE" = kenfinly2_ci ]] || { echo 'Refusing non-CI database' >&2; exit 2; }
[[ "$MAIL_MAILER" = array && "$QUEUE_CONNECTION" = sync ]] || exit 2
export COMPOSER_HOME="$source_dir/.kenfinly-cache/composer-home"
export COMPOSER_CACHE_DIR="$source_dir/.kenfinly-cache/composer-cache"
export npm_config_cache="$source_dir/.kenfinly-cache/npm"
export COMPOSER_MAX_PARALLEL_HTTP=2
export NODE_OPTIONS=--max-old-space-size=1536
install -m 600 "$CI_ENV_FILE" .env
ci_env_digest=$(sha256sum .env | cut -d ' ' -f 1)
stage=''
cleanup() {
    if [[ -f .env && $(sha256sum .env | cut -d ' ' -f 1) = "$ci_env_digest" ]]; then
        rm -- .env
    else
        echo 'Changed CI .env preserved for review' >&2
    fi
    if [[ -n "$stage" ]]; then rm -rf -- "$stage"; fi
}
trap cleanup EXIT

lock_before=$(sha256sum composer.lock package-lock.json)
php /usr/bin/composer install --prefer-dist --no-interaction --no-progress --no-scripts
php /usr/bin/composer check-platform-reqs
php /usr/bin/composer run-script post-autoload-dump --no-interaction
php artisan config:clear --no-interaction
npm ci --no-audit --no-fund
npm run test:js
npm run build
php -d memory_limit=1G vendor/bin/pest --compact --colors=never
php /usr/bin/composer install --no-dev --prefer-dist --no-interaction --no-progress --no-scripts --optimize-autoloader
php /usr/bin/composer check-platform-reqs --no-dev
[[ $(sha256sum composer.lock package-lock.json) = "$lock_before" ]] || { echo 'Lockfiles changed during build' >&2; exit 1; }

stage=$(mktemp -d "$source_dir/.kenfinly-package.XXXXXX")
git archive "$expected_sha" | tar -x -C "$stage"
cp -a vendor "$stage/vendor"
mkdir -p "$stage/public/build"
cp -a public/build/. "$stage/public/build/"
printf '%s\n' "$expected_sha" > "$stage/BUILD_REF"
python3 - "$stage" "$expected_sha" "$build_number" <<'PY'
import hashlib,json,platform,subprocess,sys
from pathlib import Path
stage=Path(sys.argv[1])
data={"source_sha":sys.argv[2],"branch":"deploy/my-kenfinly","build_number":sys.argv[3],
      "platform":platform.system()+"/"+platform.machine(),
      "php":subprocess.check_output(["php","-r","echo PHP_VERSION;"],text=True),
      "node":subprocess.check_output(["node","--version"],text=True).strip(),
      "locks":{name:hashlib.sha256((stage/name).read_bytes()).hexdigest() for name in ["composer.lock","package-lock.json"]}}
(stage/"KENFINLY_BUILD.json").write_text(json.dumps(data,indent=2)+"\n")
PY
archive="/var/lib/kenfinly-deploy/incoming/$expected_sha-$build_number.tar.gz"
[[ ! -e "$archive" ]] || { echo 'Existing artifact preserved; use a new build number' >&2; exit 1; }
temporary=$(mktemp /var/lib/kenfinly-deploy/incoming/.artifact.XXXXXX)
tar -czf "$temporary" -C "$stage" .
chmod 0644 "$temporary"
mv -n "$temporary" "$archive"
sha256sum "$archive"
