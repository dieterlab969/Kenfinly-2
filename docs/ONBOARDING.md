# KENFINLY local development on Apple Silicon

Brand: **KENFINLY** · Tagline: **Know Your Money.**

Goal: **“A new developer can run Kenfinly locally within 15 minutes.”**

This is a conditional onboarding target for an already provisioned development Mac. It is **not** a verified 15-minute fresh-Mac promise. Xcode/Homebrew installation, global runtime downloads, repository access, administrator interaction and cold dependency/browser downloads can take longer. Actual measured boundaries and results are in [LOCAL_VERIFICATION.md](LOCAL_VERIFICATION.md).

The required local URL is **https://alpha.my.kenfinly.com**. The future Ubuntu URL, `https://my.kenfinly.com`, is a separate environment: no public DNS, production database, production secret or Ubuntu deployment is configured here.

## 1. Starting assumptions and exact tested versions

The verified machine is an Apple M2 running macOS 15.5, with Homebrew under `/opt/homebrew`, Xcode Command Line Tools and administrator access. The native workflow is owner-authorized for this local task; upstream `AGENTS.md` still describes Sail. No Docker installation or global PHP/Node relinking is necessary for this workflow.

| Component | Verified installed version | Repository requirement / boundary |
| --- | --- | --- |
| PHP CLI and separate PHP-FPM | 8.5.6 | Root requires `^8.4`; locked packages require at least 8.4.1. Use `/opt/homebrew/opt/php/bin/php`, not the default XAMPP PHP |
| Composer | 2.10.0 | Installs `composer.lock`, including dev packages; no `composer update` |
| Laravel | 13.40.0 | Locked application framework |
| Node / npm | 26.0.0 / 11.12.1 | Vite requires `^20.19.0 || >=22.12.0`; this local verification also uses Node CA support. Repository CI uses Node 24; that is not the local measured matrix |
| Vue / Vite / Laravel Vite plugin | 3.5.45 / 8.3.6 / 3.2.1 | Installed from `package-lock.json`; no frontend upgrade |
| MySQL | 9.6.0 | A separate project instance. Repository Sail/CI use MySQL 8; parity is not claimed |
| Nginx / mkcert | 1.31.1 / 1.4.4 | Existing Homebrew Nginx with `include servers/*`; mkcert CA must be locally trusted |
| Mailpit | 1.31.2 | Project-specific loopback catcher, without relay/forwarding |
| Python | macOS `/usr/bin/python3` 3.9.6 | Standard library only; no pip install or virtual environment |
| Pest / PHPUnit | 5.3.5 / 13.4.5 | Existing repository tests |
| Playwright | 1.65.0 | Optional real-browser verification; matching Chromium installed locally |

Other macOS/runtime combinations may work but were not measured as this profile. Do not upgrade or relink global Homebrew packages to match this table on a Mac that hosts other projects. Provision prerequisites deliberately, verify their paths and use `./kenfinly-local doctor`. A missing prerequisite produces an error; the script does not silently install or replace global software.

Before starting, confirm:

- GitHub access to the Kenfinly repository and the **reviewed change set containing `kenfinly-local` and `docker/local/`**. At this delivery these setup changes are uncommitted in the shared working tree; the original upstream baseline alone does not contain them. Publish/merge the reviewed setup branch before onboarding someone from a remote clone. Remote publication/clone timing has not been verified.
- Nginx is installed/running, includes `/opt/homebrew/etc/nginx/servers/*`, and its site directory is writable by the developer. The shared master may be root-owned. The helper adds only one marked virtual host and never replaces existing site definitions.
- `mkcert -CAROOT` identifies a development CA already trusted by macOS. If absent, install/trust it with `mkcert -install` as an explicit prerequisite, following its administrator prompts. That fresh trust installation was not timed here. Never copy or share `rootCA-key.pem`.
- Ports 13316 (project MySQL), 19085 (project PHP-FPM), 11025/18025 (project Mailpit) and 15173 (optional Vite) are available, except an instance already owned by this checkout. Shared Nginx 80/443 may already be occupied by other local sites and is reused.
- You are using only synthetic local data. Optional cloud/AI/receipt-integration credentials are not needed.

## 2. Clone and checkout

For a newly provisioned developer, obtain the reviewed setup branch from the team:

```bash
git clone git@github.com:dieterlab969/Kenfinly-2.git
cd Kenfinly-2
git switch <reviewed-branch-containing-kenfinly-local>
git status --short
./kenfinly-local doctor
```

Replace the placeholder with a real reviewed ref; do not assume it has already been published. This checkout's audited application baseline is `e3936669c7906550024f56e61aca80cf0d834da8`. If using the current prepared checkout, skip clone/switch and preserve its uncommitted files. Do not use reset/clean to make onboarding appear successful.

Retain upstream YAFFA's MIT file, attribution and history. If needed in a new clone:

```bash
git remote add upstream https://github.com/kantorge/yaffa.git
git remote set-url --push upstream DISABLED
```

Inspect an existing `upstream` before adding it; these local settings are not transferred by clone.

## 3. Install/configure this project

For a new checkout with **no existing `.env`**:

```bash
./kenfinly-local setup
```

This uses locked Composer install and `npm ci`, checks PHP extensions/platform requirements, creates a separate MySQL instance/database, generates a first local application key, runs the unchanged schema/migrations, builds assets, creates a leaf certificate, and prepares the Nginx site. Logs/timings are private under `storage/app/kenfinly-local/`. It does not run `composer run setup`, upgrade dependencies, seed/reset an existing database or install production settings.

For this existing Day 02 checkout only, explicit adoption was used:

```bash
./kenfinly-local setup --adopt-existing-env
```

Default setup refuses an unrelated/edited existing `.env`. Adoption makes a private backup and only accepts the known Day 02 local database or already managed state. Other developers with a different existing local configuration must review/migrate it deliberately; do not keep repeating adoption against a production or unrelated environment. Stop this project's running services before rerunning dependency/setup operations.

Private local state:

- `.env`: application configuration and credentials; never commit or print it.
- `storage/app/kenfinly-local/state.json`: checkout identity and owned paths, without the application/admin passwords.
- `storage/app/kenfinly-local/mysql/`: a fresh instance's data/private admin config. This Mac reuses the verified **Day 02** data/admin paths under `storage/app/day02-local/mysql/` and database `kenfinly_day02`; no rename or reset was needed.
- New checkouts use development DB `kenfinly_local`. Both profiles use a separate `testing` database **inside that same isolated instance**, not the shared MySQL 3306 service.
- Private TLS leaf key, caches, logs and evidence stay under ignored storage. The existing application key is preserved during adoption/repeated setup.

The helper configures `APP_URL` and `ASSET_URL` to the exact HTTPS URL, host-only secure `__Host-kenfinly_alpha_session`, path `/`, HttpOnly and SameSite=Lax, and exact `SANCTUM_STATEFUL_DOMAINS=alpha.my.kenfinly.com`. It never uses `SESSION_DOMAIN=.kenfinly.com`; the local cookie must not reach `my.kenfinly.com`.

Cache/session use project files; queues use the existing `jobs`/`job_batches` tables. Redis is not required for this local profile. The database queue retry interval is 300 seconds and the worker timeout is 240 seconds. `RUNS_SCHEDULER=true` enables the repository's schedule; sandbox reset mode and incoming receipt routing remain disabled. Mail uses only `127.0.0.1:11025`.

## 4. Local hostname and trusted HTTPS

Run the single prepared administrator activation step after setup:

```bash
sudo /bin/sh "$PWD/docker/local/activate.sh"
```

It adds only a managed block resolving `alpha.my.kenfinly.com` to `127.0.0.1` and `::1`, preserves other hosts entries, validates the complete Nginx configuration, and gracefully reloads the existing master. It does not restart unrelated services or create public DNS. Conflicting mappings/site files cause an error. Enter the administrator password in your own terminal, never in chat or a source file.

The new Nginx virtual host serves only this checkout's `public/` directory through a separate PHP 8.5 FPM pool and passes correct HTTPS FastCGI parameters. Its loopback client ACL protects this site while preserving the shared wildcard listeners required by other projects. Every new project backend listener binds to `127.0.0.1`.

The leaf certificate is issued by the existing trusted mkcert development CA. TLS validation remains enabled. The helper supplies Node children with `NODE_EXTRA_CA_CERTS` pointing to the public `rootCA.pem`; Chromium and macOS clients use local trust. Do not use `curl -k`, browser certificate exceptions, `ignoreHTTPSErrors: true` or `NODE_TLS_REJECT_UNAUTHORIZED=0`.

## 5. Start, stop, background services and HMR

```bash
./kenfinly-local up
./kenfinly-local status
```

Open **https://alpha.my.kenfinly.com**. `up` starts/adopts the owned database, starts project PHP-FPM, the isolated Mailpit instance, a database worker and `schedule:work`. It is repeatable and refuses occupied unrelated ports/PIDs. Mailpit UI: `http://127.0.0.1:18025`; messages cannot be relayed externally by this configuration.

```bash
./kenfinly-local dev start   # HTTPS Vite and WSS HMR on loopback port 15173
./kenfinly-local dev stop    # return to built assets; remove only its own hot marker
./kenfinly-local restart     # app/worker/scheduler/catcher restart; retain database/data
./kenfinly-local down        # stop owned app/worker/scheduler/catcher/Vite, retain MySQL
./kenfinly-local down --database  # also stop only the verified owned MySQL instance
```

The source checkout must be on this Mac; no tunnels or LAN exposure are configured. Avoid the inherited `npm run dev` command, which kills port 5173 and binds all interfaces. The local Vite wrapper preserves the base build config, binds loopback, uses the same trusted certificate, permits the exact app CORS origin and ignores runtime/database files in its watcher.

`schedule:work` executes real repository schedules against the isolated data. Due minute jobs have been observed; not every nightly/integration job has been exercised. Do not supply production/cloud keys to make an optional integration work. Use `./kenfinly-local worker stop` / `worker start` only when diagnosing this project's queue.

When stopped, the installed Nginx site remains and may return 502 until the project FPM is started. Startup is manual; no login item or global LaunchAgent was installed.

## 6. Initial data and verification

Register a synthetic user through the HTTPS UI; default onboarding creates currencies/groups/categories, and you can add your own wallet/payee. On an **empty** development database only, optional inherited demo data is available:

```bash
./kenfinly-local seed-demo
```

It refuses to reseed if users already exist. The inherited synthetic demo login is `demo@yaffa.cc` / `demo`; it is unsuitable for any public/production environment. The application still contains YAFFA's wordmark/copy because full UI rebranding is a separate stage.

Run the checked setup verification:

```bash
./kenfinly-local browser-install  # matching Chromium; may require a large download
./kenfinly-local verify
./kenfinly-local test
```

`verify` creates a uniquely labeled synthetic user/wallet/payee, verifies trusted browser TLS, registration/login, wrong-password and missing-CSRF rejection, cookie isolation, income/expense, queued work, persistence through app restart, captured email, built assets and a real WSS HMR update. It leaves synthetic records and private evidence, and returns to built-asset mode. It does not contact production or overwrite existing records. It briefly restarts only this project's services.

The known opening-balance summary initialization gap is **not fixed**: the verification explicitly uses the application's existing full-summary endpoint and reports that workaround. Do not interpret its eventual reconciled balance as a clean fresh-account initialization pass.

`test` runs the existing Unit/Feature suite with a process-only 1 GiB limit and the existing JS tests. It targets only the isolated `testing` database; it uses synthetic test receipt routing and array mail. Full browser/Dusk coverage is separate. See [LOCAL_VERIFICATION.md](LOCAL_VERIFICATION.md) for actual results and remaining failures.

Checklist:

- Host resolver returns loopback only; HTTPS opens without a certificate warning.
- `./kenfinly-local status` passes with worker/scheduler/catcher running.
- Scripts/styles load from the HTTPS host; opt-in HMR uses HTTPS/WSS, not localhost HTTP.
- Registration/login and a synthetic wallet/income/expense workflow work.
- Data and the host-only session survive `restart`.
- Queued summary work completes; reset emails appear only in the isolated catcher.
- Relevant tests/build pass; unresolved translation/financial onboarding defects remain documented.

## 7. Common errors and fixes

| Symptom | Safe response |
| --- | --- |
| `An existing or edited .env is preserved` | Review it. Use explicit adoption only for the known local profile; never overwrite an unknown environment |
| Host missing / certificate name mismatch | Run the prepared activation command; inspect `docker/local/hostname.sh --check`. Do not change public DNS or bypass TLS |
| CA trust fails | Provision/trust mkcert on this Mac first. Do not copy another developer's CA private key |
| Node says issuer cannot be verified | Run through the helper, which passes the public local CA to Node children; do not disable validation |
| Nginx test fails on root PID permissions | The unprivileged helper uses a private PID override; final normal check/reload runs through the administrator activation helper |
| 502 at the local site | Run `up`, inspect `fpm.log` / `fpm-error.log`, confirm loopback 19085. Do not restart the shared PHP-FPM service |
| Port is occupied or PID ownership mismatch | Inspect the named port/process; the helper deliberately refuses to kill an unrelated process |
| Missing Vite manifest | Run `./kenfinly-local npm run build` in build mode |
| Stale `public/hot` after a killed Vite | Inspect its contents and the project PID. Use `dev stop` for the known owned marker; do not delete another dev server's marker |
| Wrong scheme/cookie/CSRF 419 | Confirm HTTPS app/asset URL and host-only secure cookie settings; clear only this site's browser cookies, then log in. Preserve unrelated sites/cookies |
| Jobs pending | Check the owned worker/log and `DB_QUEUE_RETRY_AFTER`; `up` starts it. Keep queue/catcher local |
| New account omits opening balance | Known baseline defect: use the existing account summary refresh/maintenance action and wait for the worker; no formula/schema fix is included |
| Full PHP test hits 128 MiB limit | Use `./kenfinly-local test`, which sets a limit only on that test process |
| Translation check fails | Existing baseline reports errors; do not upgrade dependencies or weaken tests to conceal them |

## 8. Safe local reset and rollback

Normal setup/start/stop never runs a reset. Keep data and backups by default.

Only when you explicitly intend to destroy **all synthetic development data in this checkout**:

```bash
./kenfinly-local down
./kenfinly-local db-info   # inspect exact loopback port, database and project data directory
# DESTRUCTIVE: proceed only after checking the local identity and retaining any needed backup.
./kenfinly-local php artisan migrate:fresh --seed --no-interaction
./kenfinly-local up
```

Do not use this procedure for shared/real/production data. The wrapper rejects non-local targets and checks the owned server identity; do not bypass it with a globally configured MySQL/PHP command. No forced production flag, volume deletion or database-directory deletion is needed. The isolated `testing` database is disposable and refreshed by its tests.

To undo network integration, remove only the exact marked Kenfinly Nginx site after inspecting its ownership marker, run a root Nginx config check and graceful reload, and use `sudo /bin/sh docker/local/hostname.sh --remove` for only its unchanged managed hosts block. Preserve other site files and shared CA trust. Restore an env backup only after comparing it with the current file; never replace unrelated later edits. Private backups are in ignored storage.

## 9. Time budget and measurement boundary

| Step | Planning allowance on a provisioned Mac | What is actually measured |
| --- | --- | --- |
| Access/clone/reviewed ref | 1–3 minutes, network-dependent | Remote clone/ref publication not timed |
| Prerequisite tools and CA trust | Complete before the target window | Existing installations and trusted CA inspected; fresh-Mac provisioning unverified |
| Project setup/dependencies/build | 2–8 minutes with adequate downloads/cache | This existing checkout's first HTTPS adoption took 27.22s; Composer dependencies were already installed, npm cache for this profile was new |
| Administrator hosts/Nginx activation | 1–2 minutes | Owner completed the two initial admin steps; human wait time is not included in script timings |
| Start/status | Under 1 minute | Initial process startup took 0.53s; no capacity claim |
| Optional browser download/checks/tests | Additional 2–5+ minutes | Exact final durations and cache boundaries in the verification record |

These allowances are estimates, not fresh-machine measurements. The 15-minute goal assumes the prerequisites, repository access and reviewed setup ref already exist. Cold downloads, missing privileges, port conflicts, existing incompatible configuration or first-time trust installation invalidate that assumption. See the evidence record before quoting an onboarding completion time.
