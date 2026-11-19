#!/usr/bin/python3
"""Authenticate Kenfinly hooks before the existing Jenkins GitHub integration."""

import argparse
import hashlib
import hmac
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import json
import os
from pathlib import Path
import re
from urllib.parse import parse_qs

REPOSITORY = 'dieterlab969/kenfinly-2'
DEPLOY_REF = 'refs/heads/deploy/my-kenfinly'
HOOK_PATH = '/github-webhook/'
BODY_LIMIT = 10 * 1024 * 1024


class Rejected(Exception):
    def __init__(self, status, reason):
        super().__init__(reason)
        self.status = status


def unique_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Rejected(400, 'Duplicate JSON fields')
        result[key] = value
    return result


def classify(body, content_type, event, signature, secret):
    """Return forward, ignore or ping without accessing Jenkins or changing data."""
    media_type = content_type.split(';', 1)[0].strip().lower()
    try:
        text = body.decode('utf-8')
        if media_type == 'application/x-www-form-urlencoded':
            fields = parse_qs(text, strict_parsing=True)
            if len(fields.get('payload', [])) != 1:
                raise Rejected(400, 'Exactly one payload is required')
            text = fields['payload'][0]
        elif media_type != 'application/json':
            raise Rejected(415, 'Unsupported webhook media type')
        payload = json.loads(text, object_pairs_hook=unique_fields)
    except (ValueError, UnicodeError, RecursionError):
        raise Rejected(400, 'Invalid webhook payload') from None
    if not isinstance(payload, dict):
        raise Rejected(400, 'Expected an object')
    repository = payload.get('repository', {})
    if not isinstance(repository, dict):
        raise Rejected(400, 'Invalid repository identity')
    identities = [repository.get(key, '') for key in
                  ['full_name', 'html_url', 'url', 'ssh_url', 'git_url', 'clone_url']]
    owner = repository.get('owner', {})
    if isinstance(owner, dict):
        for key in ['login', 'name']:
            identities.append(str(owner.get(key, '')) + '/' + str(repository.get('name', '')))
    elif isinstance(owner, str):
        identities.append(owner + '/' + str(repository.get('name', '')))
    pattern = r'(?:^|[/:])' + re.escape(REPOSITORY) + r'(?:\.git)?(?:$|[/?#])'
    is_kenfinly = any(isinstance(value, str) and re.search(pattern, value, re.IGNORECASE)
                     for value in identities)
    if not is_kenfinly:
        return 'forward'
    expected = 'sha256=' + hmac.new(secret, body, hashlib.sha256).hexdigest()
    if not signature or not re.fullmatch(r'sha256=[0-9a-f]{64}', signature) or not hmac.compare_digest(expected, signature):
        raise Rejected(403, 'Invalid webhook signature')
    if media_type != 'application/json':
        raise Rejected(415, 'Kenfinly requires JSON delivery')
    if str(repository.get('full_name', '')).lower() != REPOSITORY:
        raise Rejected(403, 'Conflicting repository identity')
    if event == 'ping':
        return 'ping'
    if event != 'push' or payload.get('ref') != DEPLOY_REF or payload.get('deleted') is not False:
        return 'ignore'
    sha = payload.get('after', '')
    if not isinstance(sha, str) or not re.fullmatch(r'[0-9a-f]{40}', sha) or sha == '0' * 40:
        raise Rejected(400, 'Invalid pushed commit')
    return 'forward'


class Handler(BaseHTTPRequestHandler):
    server_version = 'KenfinlyWebhook'
    sys_version = ''

    def setup(self):
        super().setup()
        self.connection.settimeout(5)

    def log_message(self, message, *arguments):
        # Never log bodies, signatures, cookies, query strings or credentials.
        return

    def respond(self, status, body, content_type='application/json'):
        delivery = self.headers.get('X-GitHub-Delivery', '')
        if self.command == 'POST':
            print(json.dumps({'delivery': delivery if re.fullmatch(r'[A-Za-z0-9-]{1,80}', delivery) else 'unavailable',
                              'action': getattr(self, 'disposition', 'rejected'), 'status': status}), flush=True)
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/up':
            self.respond(200, b'{"status":"up"}')
        else:
            self.respond(405, b'{"status":"method_not_allowed"}')

    def do_POST(self):
        try:
            if self.path != HOOK_PATH:
                raise Rejected(404, 'Unknown webhook path')
            if self.headers.get('Transfer-Encoding') or len(self.headers.get_all('Content-Length', [])) != 1:
                raise Rejected(400, 'Content length is required')
            try:
                length = int(self.headers['Content-Length'])
            except ValueError:
                raise Rejected(400, 'Invalid content length') from None
            if not 0 < length <= BODY_LIMIT:
                raise Rejected(413, 'Payload exceeds the configured limit')
            body = self.rfile.read(length)
            if len(body) != length:
                raise Rejected(400, 'Incomplete payload')
            if len(self.headers.get_all('X-Hub-Signature-256', [])) > 1:
                raise Rejected(400, 'Duplicate signature headers')
            action = classify(body, self.headers.get('Content-Type', ''),
                              self.headers.get('X-GitHub-Event', ''),
                              self.headers.get('X-Hub-Signature-256', ''), self.server.secret)
            self.disposition = action
            if action in ['ignore', 'ping']:
                self.respond(202 if action == 'ignore' else 200,
                             json.dumps({'status': action}).encode())
                return
            headers = {'Host': 'build.getkenka.com', 'X-Forwarded-Proto': 'https'}
            for name in ['Content-Type', 'X-GitHub-Event', 'X-GitHub-Delivery',
                         'X-Hub-Signature-256', 'X-Hub-Signature', 'User-Agent',
                         'X-GitHub-Hook-ID', 'X-GitHub-Hook-Installation-Target-ID',
                         'X-GitHub-Hook-Installation-Target-Type']:
                if self.headers.get(name):
                    headers[name] = self.headers[name]
            connection = http.client.HTTPConnection('10.0.0.2', 8080, timeout=5)
            try:
                connection.request('POST', HOOK_PATH, body=body, headers=headers)
                response = connection.getresponse()
                response_body = response.read(65537)
                if len(response_body) > 65536:
                    raise Rejected(502, 'Unexpected upstream response size')
                self.respond(response.status, response_body,
                             response.getheader('Content-Type', 'text/plain'))
            finally:
                connection.close()
        except Rejected as error:
            self.respond(error.status, json.dumps({'status': str(error)}).encode())
        except (OSError, http.client.HTTPException):
            self.respond(502, b'{"status":"jenkins_unavailable"}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--secret-file', type=Path)
    arguments = parser.parse_args()
    secret_file = arguments.secret_file
    if secret_file is None:
        credentials_directory = os.environ.get('CREDENTIALS_DIRECTORY')
        if not credentials_directory:
            parser.error('Supply --secret-file or a systemd credential directory')
        secret_file = Path(credentials_directory) / 'github-hmac'
    secret = secret_file.read_bytes().rstrip(b'\r\n')
    if len(secret) < 32:
        raise RuntimeError('A protected high-entropy HMAC secret of at least 32 bytes is required')
    with HTTPServer(('127.0.0.1', 19093), Handler) as server:
        server.secret = secret
        server.serve_forever()


if __name__ == '__main__':
    main()
