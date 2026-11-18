#!/bin/sh
# Manage only Kenfinly 2's loopback hostname; never edit public DNS.
set -eu

hostname='alpha.my.kenfinly.com'
begin='# BEGIN KENFINLY-2 LOCAL HOST'
end='# END KENFINLY-2 LOCAL HOST'
action=${1:---check}

case "$action" in
    --check|--install|--remove) ;;
    *) printf 'Usage: %s --check|--install|--remove\n' "$0" >&2; exit 2 ;;
esac
[ "$#" -le 1 ] || exit 2

addresses=$(awk -v target="$hostname" '{ sub(/#.*/, ""); for (i=2; i<=NF; i++) if ($i == target) print $1 }' /etc/hosts)
for address in $addresses; do
    case "$address" in
        127.0.0.1|::1) ;;
        *) printf 'Refusing conflicting hosts mapping: %s %s\n' "$address" "$hostname" >&2; exit 1 ;;
    esac
done

if [ "$action" = '--check' ]; then
    if [ -n "$addresses" ]; then
        printf '%s has loopback-only hosts entries.\n' "$hostname"
        exit 0
    fi
    printf 'Missing hosts entry. Run: sudo /bin/sh "%s" --install\n' "$0" >&2
    exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
    printf 'Administrator access is required: sudo /bin/sh "%s" %s\n' "$0" "$action" >&2
    exit 1
fi

if [ "$action" = '--install' ] && [ -n "$addresses" ]; then
    printf 'Existing loopback mapping is already suitable; no hosts changes.\n'
    exit 0
fi

umask 077
backup=$(mktemp /private/tmp/kenfinly-hosts-before.XXXXXX)
cp /etc/hosts "$backup"

if [ "$action" = '--install' ]; then
    if grep -q -F "$begin" /etc/hosts; then
        printf 'Refusing an incomplete or edited managed hosts block.\n' >&2
        exit 1
    fi
    printf '\n%s\n127.0.0.1 %s\n::1 %s\n%s\n' "$begin" "$hostname" "$hostname" "$end" >> /etc/hosts
else
    block=$(awk -v begin="$begin" -v end="$end" '$0 == begin {inside=1} inside {print} $0 == end {inside=0}' /etc/hosts)
    expected=$(printf '%s\n127.0.0.1 %s\n::1 %s\n%s' "$begin" "$hostname" "$hostname" "$end")
    if [ -z "$block" ]; then
        printf 'No owned block exists; other hosts entries were preserved.\n'
        exit 0
    fi
    if [ "$block" != "$expected" ]; then
        printf 'Refusing to remove an edited managed block; inspect /etc/hosts manually.\n' >&2
        exit 1
    fi
    temporary=$(mktemp /private/tmp/kenfinly-hosts-edit.XXXXXX)
    trap 'rm -f "$temporary"' EXIT HUP INT TERM
    awk -v begin="$begin" -v end="$end" '$0 == begin {inside=1; next} $0 == end {inside=0; next} !inside {print}' /etc/hosts > "$temporary"
    cat "$temporary" > /etc/hosts
fi

/usr/bin/dscacheutil -flushcache
/usr/bin/killall -HUP mDNSResponder 2>/dev/null || true
printf 'Updated only the Kenfinly hosts block. Previous hosts file: %s\n' "$backup"
