# KENFINLY 2.0 — home Ubuntu setup

Date: 2026-11-18 (Asia/Saigon). Public URL: **https://my.kenfinly.com**.

This is the executed native Ubuntu setup, not the Mac/Sail onboarding recipe. Use synthetic data until the known application/reporting issues and external mail limits in [DEPLOYMENT_VERIFICATION.md](DEPLOYMENT_VERIFICATION.md) are resolved. Treat this environment as production when real financial data is stored; never use local reset commands here.

## Hosts and supported runtime

The home host is `staging-server`, Ubuntu 24.04.4, Linux x86_64, reached as `sysuser@10.0.0.2` through the VPS. The historical host name does not define its data-safety policy. Existing source clone `/var/www/Kenfinly-2` was clean on `develop` at `b76d9c6b082bb8de83ab0da29fd58db5af5c2e68`; it remains separate from the release deployment and the older `/var/www/kenfinly` application.

| Component | Actual selection |
| --- | --- |
| PHP CLI / dedicated FPM | 8.4.27, `/usr/bin/php8.4`, `/usr/sbin/php-fpm8.4` |
| Composer | Existing 2.7.1, invoked through PHP 8.4; legacy deprecation notices retained |
| Node / npm | Project-specific Node 24.22.3 / npm 11.19.1 under `/opt/kenfinly-tools/node` |
| MySQL | Existing 8.0.46 binary, separate project instance/data/service |
| Nginx | Existing 1.24.0 |
| Framework | Locked Laravel 13.40.0; unchanged Composer/npm lockfiles |
| Jenkins | Existing 2.555.2 controller/executor on this host, user `jenkins` |

PHP 8.4 was installed but missing required extensions. Only its package family moved from 8.4.22 to 8.4.27 while adding bcmath, curl, mbstring, XML/DOM, ZIP and GD. No configured Nginx/cron PHP 8.4 consumer was found before this patch update. Default PHP 8.2.31 and other PHP majors remain unchanged. Shared Node 20.20.2 remains unchanged. No Docker installation, global Node relinking or mass dependency upgrade was performed.

The official Node Linux archive was pinned and SHA-256 checked before extraction. `/opt/kenfinly-tools/bin/php` selects PHP 8.4 only in this project's command-local PATH. These versions match repository CI's major runtime choices; this does not claim an identical Sail/container image.

## Directories, identities and secrets

```text
/var/www/Kenfinly-2/                       existing source clone; preserved
/var/www/kenfinly-2-deploy/
  releases/<timestamp>-<sha12>-<build>/    Linux code/vendor/assets, BUILD_REF, manifests
  current -> releases/<active>/           atomic code pointer
  previous -> releases/<compatible>/      code-only rollback pointer
  shared/.env                            persistent production configuration/key
  shared/storage/                        sessions, uploads, application/cache/log files
  shared/backups/                        private pre-migration DB dumps
/var/lib/kenfinly-mysql/                  dedicated database data
/var/lib/kenfinly-deploy/incoming/        Linux release artifacts
/etc/kenfinly/                           project configuration and private client files
/usr/local/lib/kenfinly/                 reviewed root-owned build/release entry points
```

Non-login users: `kenfinly` runs FPM/worker/scheduler; `kenfinly-deploy` owns releases/pointers; `kenfinly-db` owns only the new database data. Runtime can write shared storage and compiled bootstrap caches, not ordinary source files. Nginx can read public assets/uploads. Private storage, sessions and backups are not served by the virtual host.

| Secret location | Access / purpose |
| --- | --- |
| `shared/.env` | `root:kenfinly`, 0640; generated once, linked into every release |
| `/etc/kenfinly/mysql-admin.cnf` | root, 0600; only this new instance's administrator |
| `/etc/kenfinly/mysql-app.cnf` | `root:kenfinly`, 0640; application DB client. Database option is in `[mysql]`, not generic `[client]` |
| `/etc/kenfinly/ci.env` | root, 0600; isolated CI configuration, copied into Jenkins secret-file storage |
| `/etc/kenfinly/provision-secrets.json` | root, 0600; private initial provisioning/recovery state; never export into Git/evidence reports |
| Per-release `bootstrap/cache/config.php` | Protected bootstrap cache directory; contains resolved secrets and must not be published |

Never print these files, regenerate APP_KEY on deployment, copy Mac credentials/certificates, or seed the inherited public demo account on this environment.

## Database and supporting services

`kenfinly-mysql.service` uses `/etc/mysql/kenfinly.cnf`, binds **127.0.0.1:13316**, disables MySQL X and uses `/run/kenfinly-mysql/mysql.sock`. Databases are `kenfinly2` and `kenfinly2_ci`, with separate random users scoped to their database and loopback host. AppArmor's existing MySQL local include gained only the owned data/runtime paths. The shared MySQL 3306 service/data/credentials were not changed or used.

File cache and file sessions are project-specific; Redis is not required for this profile and the existing Redis service is untouched. Queues use the existing database tables, retry interval 300s and worker timeout 240s.

Enabled owned units:

- `kenfinly-mysql.service`
- `kenfinly-fpm.service`, loopback 19084, separate config `/etc/kenfinly/php-fpm.conf`
- `kenfinly-queue.service`, graceful SIGTERM and 300s stop allowance
- `kenfinly-scheduler.timer` with a single `kenfinly-scheduler.service` invocation per minute

Reboot persistence is configured through systemd and existing WireGuard startup ordering. No shared host was rebooted to test it. See [NETWORK_AND_DOMAIN.md](NETWORK_AND_DOMAIN.md) for the exact Nginx/UFW path.

## Configuration and first deployment

Production uses `APP_ENV=production`, `APP_DEBUG=false`, `APP_NAME=KENFINLY`, app/asset URL `https://my.kenfinly.com`, exact trusted proxy `10.0.0.1`, and host-only `__Host-kenfinly_public_session` with Secure/HttpOnly/Lax and path `/`. Email verification is **enabled**. Sandbox resets, debugbar, Telescope and unconfigured external receipt/AI integrations remain disabled/unconfigured.

Initial database setup loaded the inherited schema's 98 historical migration records and applied seven reviewed pending migrations, producing 105 historical records. The checkout has 61 migration source files; no migration/schema source was modified. `/etc/kenfinly/approved-migrations.json` records the reviewed hashes. Existing tests rebuild only `kenfinly2_ci` using its separately scoped credential; they do not reset the application database.

Routine deployment is through the dedicated Jenkins job or reviewed release entry point, not `composer run setup`, inherited `deploy.php`, a raw key-generation command or `migrate:fresh`. Missing/changed migration approvals stop publication. Initial operational provisioning scripts under private evidence storage are historical execution records, not routine startup commands.

```bash
sudo systemctl is-active kenfinly-mysql kenfinly-fpm kenfinly-queue kenfinly-scheduler.timer
sudo -u kenfinly-deploy /usr/local/lib/kenfinly/release.py status
sudo journalctl -u kenfinly-queue -u kenfinly-scheduler --since '15 minutes ago'
```

Deployment, rollback and recovery procedures are in [DEPLOYMENT_RUNBOOK.md](DEPLOYMENT_RUNBOOK.md). Full UI rebranding remains separate; the inherited YAFFA assets/copy are still visible.
