#!/bin/sh
# The only administrator step: loopback hosts entries and checked shared-Nginx reload.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
site='/opt/homebrew/etc/nginx/servers/alpha.my.kenfinly.com.conf'
[ "$(id -u)" -eq 0 ] || { printf 'Run: sudo /bin/sh "%s"\n' "$0" >&2; exit 1; }
[ -f "$site" ] || { printf 'Run ./kenfinly-local setup first.\n' >&2; exit 1; }
grep -q -F "# Managed by Kenfinly local: $root" "$site" || { printf 'Unrelated site preserved.\n' >&2; exit 1; }
/bin/sh "$root/docker/local/hostname.sh" --install
/opt/homebrew/bin/nginx -t
/opt/homebrew/bin/nginx -s reload
printf 'Activated only the prepared Kenfinly hostname/site; existing Nginx master was gracefully reloaded.\n'
