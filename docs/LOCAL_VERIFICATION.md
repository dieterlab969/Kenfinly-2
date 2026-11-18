# KENFINLY local environment — verification record

Date: 2026-11-18 (Asia/Ho_Chi_Minh) · Day 03\
Application baseline: `e3936669c7906550024f56e61aca80cf0d834da8`, branch `develop`\
Local URL: **https://alpha.my.kenfinly.com**\
Result: **Local HTTPS development works, with the pre-existing opening-summary workaround explicitly required. Not production/release approval.**

## 1. Scope and evidence boundary

Reviewed `AGENTS.md`, README, the Day 01/02 plans/reports, manifests, lockfiles, environment examples, CI/Sail configuration and installed tooling before implementation. `.ai/rules` does not exist. Updated `CHANGE_PLAN.md` before changes. The existing owner-approved native approach was reused for this local task; the Sail instructions themselves were not edited.

This Mac is Apple M2 / arm64, macOS 15.5. Exact installed/locked versions are listed in [ONBOARDING.md](ONBOARDING.md). Execution uses explicit Homebrew PHP 8.5.6, Composer 2.10.0, Node 26.0.0 / npm 11.12.1 and MySQL 9.6.0. This differs from repository CI's PHP 8.4 / Node 24 / MySQL 8 matrix. Composer's platform check passes; CI parity is unverified.

No new commit or push was made. The original application source, financial calculations, schema/migration files, dependency manifests/lockfiles, branding graphics, MIT license and prior dated reports remain unchanged. Existing Day 01/02 working-tree documentation was preserved. Setup changes must be reviewed/published before another developer can obtain them from a remote clone.

Raw evidence lives under ignored `storage/app/kenfinly-local/`; earlier baseline evidence remains under `storage/app/day02-local/`. These are local artifacts, not committed attachments. Private environment backups, generated synthetic login credentials, session logs, database files and TLS keys must stay ignored. Public reports contain no secrets.

## 2. Actual configuration

| Component | Verified configuration |
| --- | --- |
| Hostname | `/etc/hosts` managed block maps only to `127.0.0.1` and `::1`; system resolver returns those addresses |
| Front door | Existing shared Nginx 1.31.1, one new owned virtual host, HTTP redirect to HTTPS |
| Access | HTTPS site allows loopback clients only; a request from this Mac's non-loopback address returned **403**, with valid TLS |
| TLS | New mkcert leaf for the exact hostname, existing locally trusted CA; normal validation enabled |
| PHP | Separate project PHP-FPM pool on `127.0.0.1:19085`; shared FPM configuration unchanged |
| Database | Owned instance `127.0.0.1:13316`, private socket `/private/tmp/kenfinly-day02-mysql.sock`, original project data directory retained |
| DB names | Existing development DB `kenfinly_day02`; separate disposable `testing` DB on the same isolated instance. New checkouts use `kenfinly_local` |
| URL/assets | `APP_URL` and `ASSET_URL` use the exact HTTPS origin; FastCGI conveys HTTPS correctly |
| Session | File driver, `__Host-kenfinly_alpha_session`, Secure, HttpOnly, path `/`, SameSite=Lax, no Domain attribute |
| CSRF/Sanctum | Existing CSRF protection retained; exact local stateful hostname |
| Cache/queue | Project file cache; existing database queue; retry interval 300s, worker timeout 240s |
| Scheduler | Owned `schedule:work`, `RUNS_SCHEDULER=true`, sandbox resets disabled; no integration keys added |
| Mail | Owned Mailpit 1.31.2, SMTP `127.0.0.1:11025`, UI `127.0.0.1:18025`; no relay/forwarding configured |
| Development assets | Opt-in Vite HTTPS on `127.0.0.1:15173`, exact app CORS origin and WSS HMR |

The owner completed the two administrator helpers for the hosts block and checked Nginx graceful reload. No public DNS record was created. Existing Nginx wildcard listeners were preserved for other local sites; all newly started backend listeners bind loopback. No shared MySQL data, global PHP configuration, runtime symlink, shell profile, Homebrew service or LaunchAgent was changed. The confirmed old Day 02 server on port 18080 was retired after HTTPS worked.

## 3. Executed checks

| Check / command | Actual result | Local evidence |
| --- | --- | --- |
| `./kenfinly-local doctor` and installed package/lock inspection | Exact runtime/package versions confirmed before use | Initial inspection and `setup-first.log` |
| `./kenfinly-local setup --adopt-existing-env` | Success; private backup, existing APP_KEY/data retained, locked install/build/migrations, new TLS/FPM/Nginx configuration | `evidence/setup-first.log`; per-stage logs |
| Composer `install --no-scripts`, `check-platform-reqs`, existing post-autoload script | Exit 0; no dependency upgrade; package discovery passes | `composer-install.log`, `platform-check.log`, `package-discovery.log` |
| `npm ci --no-audit --no-fund`; `npm run build` | Exit 0; 324 locked npm packages; Vite 8.3.6 build succeeds | `npm-ci.log`, `build.log` |
| Shell/Python/Node syntax checks | Both shell helpers, Python entry point and both `.mjs` files pass | Commands: `sh -n`, Python `compile`, `node --check` |
| Hosts helper `--check`; resolver | Loopback-only entries and `::1` / `127.0.0.1` resolution | `evidence/verification.json` |
| macOS `security verify-cert` for CA and hostname leaf | Success; existing local CA trusted, exact hostname certificate accepted | `ca-trust.log`, initial TLS inspection |
| Normal curl `/login`, `/up` | Both **200**, TLS verification result **0**; no insecure flags | `evidence/https-and-existing-sites.json` |
| Boost `GetAbsoluteUrl` for login | Resolves `https://alpha.my.kenfinly.com/login` | `evidence/absolute-url.json` |
| `./kenfinly-local status` | FPM, catcher, worker, scheduler running; built-asset mode; trusted health check passes | Final handover check |
| Real Chromium registration/login | Form registration succeeds; wrong password rejected; fresh browser login succeeds; TLS 1.3 with validation enabled | `evidence/verification.json` |
| Cookie isolation | Exact host-only secure session; browser cookie selection for `my.kenfinly.com` is empty, without requesting that site | `evidence/verification.json` |
| Missing-CSRF POST | **419**, rejected | `evidence/verification.json` |
| Synthetic wallet/income/expense | Authenticated real HTTPS endpoints: USD opening 500, income 150, expense 30; stored amounts checked | `evidence/verification.json` |
| Queue processing | Worker paused, existing full-summary endpoint returns **202**, five queued jobs observed, worker resumed, resulting native balance **620** | `evidence/verification.json`, `worker.log` |
| Restart persistence | Owned app/catcher/worker/scheduler restarted; existing browser session and stored expense remain available | `evidence/verification.json` |
| UI after DB restoration/repeated setup | Fresh browser login succeeds; both synthetic transactions are visible in account history | `evidence/post-setup-ui.json`, `evidence/wallet-history-https.png` |
| Local email | Password-reset request captured for a unique `example.test` address; no external mail transport used | `evidence/verification.json`; private catcher database |
| Real HMR | HTTPS dev modules load, WSS connects, temporary module changes **initial → updated**; temporary probe removed and built mode restored | `evidence/verification.json`, `vite.log` |
| Built/dev assets and browser errors | No failed script/style/font/image responses or page exceptions in the successful run | `evidence/verification.json` |
| Scheduler | Due minute Google Drive monitor/AI-document commands execute successfully against synthetic local state; no integration credentials supplied | `scheduler.log`, `worker.log` |
| `./kenfinly-local test` | **1,806 PHP tests passed, 6,427 assertions; 40 JS tests passed**, exit 0 | `test-php.log`, `test-js.log`, `evidence/tests-final.log` |
| Fresh database bootstrap | New scratch data directory initialized and secured; unchanged schema/migrations load successfully; 0 users | `evidence/fresh-bootstrap-check.json`; scratch `fresh-migrate.log` |
| Original database restoration | Original 48 users / 114 transactions / 43 account entities retained before/after scratch check and repeated setup | `evidence/fresh-bootstrap-check.json`, `evidence/retention-and-repeatability.json` |
| Repeated setup/start | Stops owned services, setup succeeds again; Nginx site unchanged, no new reload; repeated `up` keeps the same owned PIDs | `evidence/setup-repeat.log`, `evidence/up-repeat.log`, `evidence/retention-and-repeatability.json` |
| Unsafe configuration guards | Temporary checkout stub: existing env refused; explicit production adoption refused; foreign checkout state refused; env bytes unchanged | `evidence/guard-checks.json` |
| Private files | Env, state, leaf private key and DB admin config are mode 0600 and ignored | `evidence/guard-checks.json`; Git ignore checks |
| Other local sites | Original Nginx config/site checksums unchanged; original master/shared FPM/MySQL/Mailpit processes retained; three old sites return 301, blog site 200 | `evidence/https-and-existing-sites.json`; `/private/tmp/kenfinly-day03-nginx-before.sha256` |

Registration/login and rendered pages are browser interactions. Wallet/payee creation and income/expense use the application's real authenticated endpoints through the browser request context, not direct model/SQL writes. These do not claim that every financial form was manually clicked. Day 02's existing critical/report browser suites (27 tests) and transfer/edit fixture remain historical evidence; they were not rerun as a complete browser suite today.

Screenshots: `evidence/wallet-https.png`, `evidence/wallet-history-https.png` and `evidence/dashboard-https.png`, visually inspected. They show the real inherited YAFFA UI and the local USD 620 balance. Full display rebranding has not been performed.

Migration-count clarification: the checkout contains **61 migration source files**, while the loaded schema's migration table contains **105 historical records**, also reproduced by the fresh scratch database. Day 02's phrase “61 recorded migrations” referred to the status listing and was imprecise. That dated report is preserved; no migration was added to produce this difference.

## 4. Measured timings

Wall times below are actual command measurements. Per-stage monotonic timings and exit codes are in `timings.jsonl`.

| Measurement | Observed time | Boundary |
| --- | --- | --- |
| First adoption/setup for HTTPS | **27.22s** | Existing checkout, installed Composer dependencies and runtimes, existing project DB and trusted CA; this profile's npm cache was new |
| First owned service startup | **0.53s** | Database already running; excludes owner administrator interaction |
| Final complete HTTPS/browser check | **12.86s** | Matching Chromium already downloaded; includes synthetic flows, restart, mail and real HMR |
| Existing PHP+JS test command | **74.04s** | PHP runner reports 73.27s; test-process-only 1 GiB limit; isolated test DB |
| Scratch fresh database provisioning | **3.331s** | New empty data directory, installed MySQL binary; no package download |
| Scratch inherited schema/migrations | **0.839s** | Empty scratch database; no application code changes |
| Repeated owned-service stop | **0.77s** | Data retained; project MySQL stays running |
| Repeated setup | **19.77s** | Warm dependency cache; preserves env/key, data and certificate/site; no administrator reload |
| Repeated owned service startup | **0.38s** | Database already running |

These measurements are **not** an end-to-end onboarding time and should not be summed into a fresh-Mac claim. Remote access/clone, reviewed-ref publication, Xcode/Homebrew installation, cold runtime/dependency/browser downloads, initial CA trust and human administrator time were not measured. Fresh database provisioning was tested separately; a complete clean-checkout setup on a second Mac was not. The 15-minute onboarding goal is conditional on the explicit provisioned-Mac assumptions in the guide.

## 5. Failures, corrections and remaining limits

- Initial Node API requests rejected the local issuer even though macOS curl and Chromium trusted it. The system-CA flag alone did not reach Playwright's API driver. The helper now supplies the already trusted **public** CA through `NODE_EXTRA_CA_CERTS`; validation stays enabled. No CA private key was read/shared.
- Verification-harness assumptions were corrected from observed behavior: use a fresh browser session for login, create the payee explicitly, accept asynchronous summary status 202, and wait for the secure HMR connection before editing a temporary multiline probe. Initial diagnostic failures remain locally recorded; only the final successful run is labeled passed. The application was not modified to satisfy these checks.
- **D02-F01 remains open:** a new account's initial derived summary can omit the stored opening balance. The test explicitly requests the existing full-summary rebuild before expecting USD 620. This is a documented workaround, not a successful unassisted fresh-account report test or a financial fix.
- The unchanged translation checker previously returned **308 errors / 91 warnings** on Day 02. It remains an unresolved baseline failure; no locale cleanup was performed or claimed today.
- Full Dusk/Pest browser, multiple browsers, manual Safari, mobile/dark-mode review, all nightly tasks and optional external integrations were not verified. The in-app browser backend was unavailable; the repository's locked Playwright Chromium was used instead.
- Official Sail/CI runtime parity, security/dependency-license distribution audit and capacity planning remain separate work. No production or Ubuntu deployment was performed.
- Setup scripts/docs remain uncommitted in this checkout. A new developer cannot obtain them from the baseline remote ref until the reviewed change set is published.

## 6. Handover

```bash
./kenfinly-local up
./kenfinly-local status
./kenfinly-local dev start   # optional HTTPS/WSS development mode
./kenfinly-local dev stop    # built assets
./kenfinly-local down        # retain database and data
./kenfinly-local down --database  # also stop the owned database, retain data
```

The application is left running at **https://alpha.my.kenfinly.com**, with worker, scheduler and catcher active, and Vite stopped in built-asset mode. No further administrator action is required for the current configuration. Use only synthetic data. Continue local development; resolve the documented baseline defects and review/publish setup before wider onboarding. Deployment and production changes require separate approval.
