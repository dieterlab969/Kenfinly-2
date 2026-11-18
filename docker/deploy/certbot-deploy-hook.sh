#!/bin/sh
# Existing global renewal timers may invoke this; act only for this lineage.
set -eu
if [ "${RENEWED_LINEAGE:-}" = /etc/letsencrypt/live/my.kenfinly.com ]; then
    /usr/sbin/nginx -t
    /bin/systemctl reload nginx
fi
