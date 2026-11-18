# KENFINLY 2.0 — deployment and recovery runbook

Applies only to the public Ubuntu deployment at **https://my.kenfinly.com**. The Mac alpha profile is separate. Preserve real financial data as production data regardless of the server's historical staging name.

## Normal deployment

1. Review the exact develop commit, dependency lockfiles and any migration changes. Do not upgrade dependencies or change financial behavior as a deployment shortcut.
2. Open the dedicated Jenkins job and choose `ACTION=deploy`. Leave migration approval false unless pending migrations were explicitly reviewed and their hashes installed by the operator.
3. Confirm Linux tests/build/platform checks pass, publication succeeds, the active SHA matches the selected commit, and public health/login checks return 200 with normal TLS verification.
4. Check the owned worker/timer and relevant logs. Verify a dedicated synthetic flow when appropriate, without using real financial data for smoke tests.

```bash
sudo -u kenfinly-deploy /usr/local/lib/kenfinly/release.py status
sudo systemctl is-active kenfinly-mysql kenfinly-fpm kenfinly-queue kenfinly-scheduler.timer
curl --fail --silent --show-error https://my.kenfinly.com/up --output /dev/null
```

The root-owned release helper accepts only its exact incoming artifact path/SHA/build identity. It links persistent env/storage, prepares caches before publication and switches the current symlink atomically. Normal startup/deployment does not seed, reset, rotate keys, delete uploads or rebuild the application database.

## Migration approval

Approval file: `/etc/kenfinly/approved-migrations.json`. Before approving new files, inspect their operations, data effects and older-code compatibility. Record the intended migration and rollback/recovery decision. A checkbox alone cannot approve an unknown migration hash.

The helper makes an owned, private mysqldump backup before an approved apply, enters project maintenance mode when necessary, then runs the existing `migrate --force`. It never runs `migrate:fresh` or down-migrations against the application database. Existing tests may reset **only the separate CI database**, whose user has no application-database grant.

Backups are under `shared/backups`, owner-only directory and mode-0600 SQL files. Verify a backup completed and belongs to this DB before any separate recovery exercise. Failed/partial initial attempts are retained as diagnostic artifacts, not valid restore candidates. **No automatic rollback restores a backup over live data.**

## Code rollback

Preferred audited path: Jenkins `ACTION=rollback`, with migration approval false. Emergency operator path:

```bash
sudo -u kenfinly-deploy /usr/local/lib/kenfinly/release.py status
sudo -u kenfinly-deploy /usr/local/lib/kenfinly/release.py rollback
```

The helper requires a health-verified previous release and matching schema fingerprint, refreshes target caches against the current shared `.env`, switches code, reloads the dedicated FPM, gracefully restarts the worker and checks public HTTPS. The previous pointer then references the release just left; a second rollback can return to it. Inspect status before every operation rather than assuming the pointer's chronological direction.

If schema compatibility differs, rollback stops and requires an operator decision. Never force it by editing the fingerprint, rewinding the database, generating a new key or dropping tables. Migration rollback/point-in-time recovery is separate, explicit work requiring assessment of data written since deployment.

After switching, verify login/session continuity, expected synthetic records/balances and persistent storage. Check the active SHA and Jenkins archived manifest. Network/TLS/firewall settings remain in place during code rollback.

## Failure diagnosis

| Symptom | Action |
| --- | --- |
| Build/platform/test failure | Keep current release serving; inspect the failed stage. Fix setup or reviewed source, not the tests/lockfiles to hide a failure |
| Unknown pending migration | Review and approve exact hashes; do not rerun with a blanket force/reset |
| 502 | Inspect `kenfinly-fpm`, its private storage log, Nginx error log and loopback 19084; do not restart shared FPM pools |
| Maintenance remains active | Inspect failed migration/publication state before bringing the project up; retain DB backup and failure logs |
| Wrong URLs/cookie/CSRF | Check fixed edge forwarding, trusted peer, exact HTTPS URL and host-only cookie; do not broaden trusted proxies or cookie domains |
| Email failure | Inspect the owned WireGuard SMTP path and dedicated mailbox. External delivery is separate from local transport; keep verification enabled |
| Wrong starting runtime | Use project command-local PATH and PHP 8.4, not global PHP 8.2 or Mac binaries |
| New-account balance omits opening amount | Known D02-F01. Existing full-summary action is a documented workaround, not a financial/schema fix |

Private logs: home `/var/log/nginx/kenfinly2.*`, `shared/storage/logs/`, and `journalctl -u kenfinly-*`; VPS `/var/log/nginx/kenfinly2-edge.*` and normal Postfix logs. Signed links, cookies, complete env files and financial records must not be pasted into public reports. APP_DEBUG stays false while investigating.

## Services, reboot persistence and decommission

Only owned units may be started/stopped for this project. They are enabled, with one scheduler timer and existing WireGuard boot ordering. No reboot was performed as a test. Verify units/tunnel/HTTPS after a future planned reboot.

Full infrastructure rollback is separate from code rollback. Review backups under `/var/backups/kenfinly-2/20261118-before`, restore/remove only the target vhosts/owned drop-ins/exact ingress rule, test Nginx on each host before graceful reload, and preserve all unrelated sites/routes/peers. For SMTP, remove only the marked master.cf block and owned sender map after Postfix checks; do not disable other mail domains. Retain data, keys, uploads, certificates and the test mailbox by default. No automatic data/release pruning was introduced.
