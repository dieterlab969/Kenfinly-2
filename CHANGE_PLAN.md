# KENFINLY 2.0 — Safe Fork and Rebranding Change Plan

Date: 2026-11-16 (Asia/Ho_Chi_Minh)\
Last reviewed: 2026-11-18 (Day 03)\
Baseline: `e3936669c7906550024f56e61aca80cf0d834da8` (`develop`)\
Product: **KENFINLY**\
Tagline: **Know Your Money.**\
Status: Day 03 isolated HTTPS development is running and verified within the recorded scope. Initial summary-cache and translation defects remain open. Full UI rebranding has not started.

## Day 03 implementation plan — local HTTPS and onboarding, 2026-11-18

Recorded before implementation changes. The owner now explicitly requests the local hostname `https://alpha.my.kenfinly.com`, trusted HTTPS, operational workers/scheduler, reproducible scripts and English documentation. This extends the previously approved native development approach for this task: reuse the installed Apple Silicon tooling instead of installing Docker or changing global PHP/Node services. `AGENTS.md` remains unchanged. Creating `docs/ONBOARDING.md`, `docs/LOCAL_VERIFICATION.md`, a dated Day 03 report and local setup scripts is authorized by the request and the standing reporting convention.

### Inspection and preservation baseline

- Source remains `e3936669c7906550024f56e61aca80cf0d834da8`. Preserve the modified README and all untracked Day 01/02 deliverables. Do not commit, push, replace history or touch production.
- `.ai/rules` is absent. Read the committed instructions and Day 01/02 documents. Lock metadata records Laravel 13.40.0, Vue 3.5.45, Vite 8.3.6, Laravel Vite plugin 3.2.1, Pest 5.3.5, PHPUnit 13.4.5 and Boost 2.10.4. Confirm installed executables/dependencies before relying on their APIs.
- Existing native tools include PHP 8.5.6, Composer 2.10.0, Node 26.0.0, npm 11.12.1, MySQL 9.6.0, Nginx 1.31.1, mkcert 1.4.4 and Mailpit 1.31.2. The default `/usr/local/bin/php` points to XAMPP; use the explicit Homebrew PHP binary.
- Existing Nginx virtual hosts for `alpha.kenfinly.com`, `alpha.kenkai.vn`, `alpha.creatorplan.kenkavn.com` and `blog-dev.kenkai.vn` must remain byte-identical. Their shared wildcard listeners must not be narrowed or replaced, which would disrupt other sites. Restrict the new virtual host to loopback clients; bind every new project process to loopback. Preserve the current PHP-FPM, MySQL 3306 and Mailpit 1025/8025 services.
- Day 02 owns MySQL 13316, `storage/app/day02-local/mysql/data`, and its private admin configuration. Preserve its data and reuse it only after verifying the live data directory/socket/port. The existing development `.env` is local and may be updated for this task after a private backup; keep its existing application key.
- `/etc/hosts` does not yet contain the required hostname and is root-owned. `sudo -n true` reports that a password is required. A concrete minimal helper will be supplied for the owner to run with administrator rights if that remains necessary; do not obtain the password or bypass OS permissions.

### Implementation register

| ID | Change and reason | Risk and control | Verification | Rollback |
| --- | --- | --- | --- | --- |
| D03-01 | Add repeatable local orchestration in the existing `docker/local/` area, with a root `kenfinly-local` entry point | Refuse unexpected ports/PIDs, non-local DB targets, conflicting env/site files and overwrite of unknown state. Existing configuration is adopted only explicitly, with private backup. No bulk dependency updates | Run syntax checks, setup twice, conflict guards, start/stop/restart and record actual timings | Stop only matching owned processes; retain data. Reverse only task-owned source files; preserve previous documents |
| D03-02 | Configure `alpha.my.kenfinly.com` through a managed hosts-file block and existing trusted mkcert CA | Administrator permission and trust may need owner action. Add only loopback entries; reject conflicting non-loopback mappings. Do not create public DNS, change other host entries, expose/sign with a production key or disable TLS checks | System resolver, certificate SAN/chain, normal TLS-verifying HTTP client and browser navigation | Remove only the managed hosts block/new certificate/site; do not remove the shared CA trust or other hosts |
| D03-03 | Add one Nginx site using project-local certificate and a separate PHP 8.5 FPM pool on loopback | Existing Nginx serves other projects. Back up/check hashes, reject an unrelated site-file collision, test full config before graceful reload. Use FastCGI HTTPS parameters rather than broad proxy trust | `nginx -t`, old-site smoke checks, new HTTPS/login/health and asset requests | Remove only the owned virtual host, validate and gracefully reload; stop only project FPM; preserve all old sites |
| D03-04 | Update ignored `.env` with HTTPS app/asset URL, host-only secure uniquely named session cookie, exact Sanctum origin, SMTP catcher, database queue and file cache | Preserve application key and existing DB data. Use no production credentials or cookie domain shared with `my.kenfinly.com`; no TLS bypass. Back up and reject silent overwrite | Effective framework config, Secure/HttpOnly/SameSite/host-only cookies, registration/login/CSRF and origin behavior | Restore the private prior env backup only after comparing the current managed revision; clear only project config cache and restart owned processes |
| D03-05 | Isolate local Mailpit on loopback ports 11025/18025; run project DB worker and scheduler | Do not alter shared Mailpit/Redis/Homebrew services or introduce SMTP relay. Scheduler may run real repository jobs, but only on the isolated synthetic DB with no external integration keys; sandbox resets stay off | Captured test email, queue backlog→processed evidence, schedule listing and due-job execution | Stop only owned worker/scheduler/catcher; keep captured synthetic evidence and data |
| D03-06 | Add opt-in local Vite configuration using the same trusted certificate, exact HTTPS origin and secure WebSocket HMR | Do not execute existing `npm run dev` port-killing behavior or change the base bundler defaults for other environments. Bind to loopback and fail on port conflicts | HTTPS module requests, browser WebSocket connection and real hot update; then stop HMR and verify built assets | Stop only owned Vite and remove its own hot-file entry; keep normal build behavior |
| D03-07 | Exercise real synthetic registration/login, wallet/income/expense, persistence through app restart, background work and relevant existing tests | Preserve Day 02 data; do not change financial calculations or schema. The known opening-summary gap remains a defect, with only the existing rebuild operation allowed | Real HTTPS and browser/HTTP evidence; unchanged lock/license/source hashes; test/build exit codes | Retain synthetic records by default; no schema redesign, financial fix or broad data reset |
| D03-08 | Create English onboarding/verification docs and Day 03 daily record; measure actual executed steps | The 15-minute objective is conditional on explicit prerequisites; do not claim cold downloads, fresh macOS setup or an unpublished checkout ref were timed | Report provisioned-Mac measurements, first-use versus repeated setup, download/cache boundaries, blockers and exact tested versions | Keep historical reports; reverse only inaccurate new documentation |

Planned project endpoints, subject to port-conflict checks: required HTTPS host on shared Nginx 443 (loopback client ACL), separate PHP-FPM 127.0.0.1:19085, existing isolated MySQL 127.0.0.1:13316, local mail SMTP/UI 127.0.0.1:11025/18025 and opt-in Vite HTTPS 127.0.0.1:15173. New runtime state, backups, TLS private files and evidence remain under ignored `storage/app/kenfinly-local/`. No production setting for `https://my.kenfinly.com` is installed or contacted.

Additional inspection before activation: the shared Nginx master is root-owned, so its graceful reload also needs the owner's administrator action. An unprivileged syntax check can use a private PID-file override; the final activation helper will run the normal root syntax check and reload without restarting the service. The existing mkcert root CA is already trusted according to macOS `security verify-cert`; reuse it, generate only a new leaf certificate, and never read/export the CA private key. Standard-library orchestration uses the existing `/usr/bin/python3` 3.9.6, with no pip dependencies or global Python install.

Verification adjustment before retry: macOS curl and Chromium successfully validate the new certificate, and browser registration succeeded. The Node 26 API client rejected the issuer because its default bundled CA list excludes the Mac's trusted local CA. Invoke the local verification process with Node's supported `--use-system-ca` option; do not disable verification or change global Node settings. Preserve the failed attempt as a trust-store diagnosis. Limit error artifacts to sanitized messages, not browser session-cookie call logs.

The system-CA flag alone did not propagate the required trust to Playwright's Node API driver. Following mkcert's Node guidance, pass `NODE_EXTRA_CA_CERTS` pointing only to the already trusted local CA's **public** `rootCA.pem` in the helper's child-process environment. This adds an issuer to normal chain/hostname validation; it does not disable either validation and does not copy the CA private key. Record both unsuccessful client configurations and the successful final configuration in the verification document.

After verifying the HTTPS replacement, retire only the confirmed Day 02 `artisan serve --port=18080` parent/child from this checkout. Recheck their command, user and working directory before TERM; never signal the shared FPM/Nginx services. Rollback is the archived Day 02 startup command; the new HTTPS service and retained data remain available.

Additional verification scope, recorded before execution: validate the new-checkout database bootstrap in a separate ignored scratch directory, after the current test run completes. Stop only this checkout's owned application/database, initialize and secure a new synthetic instance on the checked project port, run the unchanged migrations against it, then shut it down and restore the original Day 02 instance. Never initialize over or delete the original data directory. Compare original row counts, application-key identity, certificate and Nginx hashes before/after. The risk is temporary local downtime or a failed scratch process; rollback is verified shutdown of the scratch instance followed by `./kenfinly-local up` using the retained original state. This tests fresh database provisioning, not a fresh Mac or cold remote clone. Also run repeat setup with the owned services stopped and verify that it neither resets data nor requires a new Nginx reload. Disposable guard checks may use a separate temporary checkout stub and must never edit the real `.env` to simulate unsafe targets.

### Day 03 execution outcome

Completed the owned native HTTPS profile, helpers/templates, host-only secure session, isolated mail catcher, worker/scheduler and opt-in HTTPS/WSS development mode. Owner ran the prepared administrator hosts/reload steps. Normal curl and Chromium validate the certificate without a bypass; HTTPS login/health return 200 and non-loopback HTTPS returns 403. Registration/login, wrong-password rejection, CSRF rejection, cookie isolation, synthetic wallet/income/expense, queue completion, restart persistence and captured reset mail have executed evidence. Real WSS hot update passes, temporary source probe removed, built mode restored.

The unchanged default suite passes: 1,806 PHP tests / 6,427 assertions and 40 JS tests; locked build/platform checks pass. Repeated setup succeeds in 19.77s without another Nginx reload; repeated start keeps owned PIDs. Fresh scratch database initialization/migrations pass and the original database is restored, with 48 users / 114 transactions / 43 account entities unchanged. Original APP_KEY matches the private pre-adoption backup. Existing shared services and original Nginx files remain preserved. The superseded project HTTP server on 18080 is stopped. Original license, locks, financial/schema source and Day 01/02 reports are unchanged.

First HTTPS adoption took 27.22s and initial service start 0.53s on this provisioned checkout; these exclude cold-Mac/tool/trust/clone/admin time. Full fresh-Mac or remote-clone onboarding within 15 minutes is unverified. The known D02-F01 opening-summary gap remains and is explicitly worked around only through the existing full-summary endpoint; translation failures remain open. See `docs/ONBOARDING.md`, `docs/LOCAL_VERIFICATION.md` and `DAY_03_REPORT.md` for exact measurements, command evidence, failure corrections and handover. No commit, push, public DNS or production/deployment change was made.

The following Day 01/02 sections are historical evidence and constraints. Record deviations and outcomes in this amendment and `docs/LOCAL_VERIFICATION.md` as execution proceeds.

## Day 02 amendment — 2026-11-17, local setup and baseline verification

This amendment is recorded before installing dependencies, creating local environment files, starting project services or writing sample data. The Day 01 sections below remain a dated record of the initial plan, not a claim that their proposed work has been performed.

### Reviewed starting state

All five requested Day 01 documents are present, plus `DAILY_REPORT.md`. They are untracked working-tree files, not committed deliverables. The only modified pre-existing tracked file is `README.md`. `HEAD` and the existing local `upstream/develop` ref remain `e3936669c7906550024f56e61aca80cf0d834da8`; no Day 01 implementation commit exists. The original license, application code, schema, Composer/npm lockfiles and graphics remain unchanged. The actual runtime still displays YAFFA. Installation, build and application tests were not completed on Day 01.

Read-only Mac discovery found arm64 macOS 15.5, Homebrew PHP 8.5.6 (separate from the default XAMPP PHP executable), Node 26.0.0, MySQL 9.6.0, Composer and Mailpit. Existing MySQL, nginx, PHP-FPM and Mailpit listeners belong to the pre-existing environment and must not be stopped or reconfigured. Docker/Colima/OrbStack were not found on PATH or in the checked standard application locations. No software has been installed by this Day 02 task at this point.

### Scope, reasons, risks, verification and rollback

| ID | Scope and reason | Risks and controls | Verification | Rollback |
| --- | --- | --- | --- | --- |
| D02-01 | Recheck Day 01 files against Git, actual source, lock metadata and license; preserve the Day 01 report | Untracked documentation is easily mistaken for a completed commit; proposed changes are not installed behavior | Record actual HEAD/diff/remotes, checksums and discrepancies in the Day 02 report | Reverse only Day 02 documentation edits; keep Day 01 artifacts and unrelated work |
| D02-02 | Select an isolated Mac ARM64 runtime based on existing installations and exact lock requirements | `AGENTS.md` mandates Sail. Native PHP/Node is a deviation requiring the owner's choice; do not create a fake Sail wrapper. A global Docker/runtime installation is outside project-only dependency installation | Check available versions, platform requirements and repository CI/runtime configuration; record the chosen exception or Sail bootstrap explicitly | Stop only task-owned processes; no global PHP, Node, MySQL, nginx, PATH or Homebrew service changes |
| D02-03 | Install exact Composer/npm lockfile contents into ignored `vendor` / `node_modules`; use a project-scoped cache if needed | Composer lifecycle hooks and npm scripts can execute code. Inspect scripts first; never update lockfiles or bypass real platform requirements. Do not use `composer run setup` | Install exit codes, installed package versions, platform check, lockfile checksums and build | Remove only task-created dependency/build/cache artifacts if requested; lockfiles/manifests stay unchanged |
| D02-04 | Create ignored local configuration only for this checkout, with no real credentials or external import/AI keys | The Day 02 setup request authorizes new project-local configuration; do not overwrite an existing `.env`. Bind app/database to loopback on unused ports and disable scheduler/external processing | Confirm target environment, database names, port ownership and local-only configuration before migration/test | Stop project processes and remove only the new ignored configuration; never rotate keys or edit any other project's files |
| D02-05 | Start a separate database instance/data directory or dedicated Sail database, with separate development and test databases | Never run tests/migrations against the existing MySQL service. Existing test configuration uses the generic `testing` DB name; isolate the entire instance and review test overrides before running | Confirm connection/server port and isolated data directory, inspect schema read-only, run only inherited migrations on the new empty instance | Stop only the owned instance. Retain its data/evidence by default; delete its confirmed disposable data only on explicit cleanup. Do not run down-migrations or delete shared volumes |
| D02-06 | Verify login, money accounts, opening balances, income, expense, transfer, edit and balance report using synthetic data | Financial calculations/schema are protected. Use existing tests/factories and real UI where available; do not substitute proposed checks or seed assumptions for executed results | A deterministic fixture: cash 1,000 + income 250 − edited expense 50 − transfer 100 = 1,100; bank 500 + transfer 100 = 600; total 1,700 in one currency. Also verify wrong-password rejection and account/transaction persistence | Remove only synthetic records in the isolated instance if needed, or retain the disposable instance; no application finance/schema code changes |
| D02-07 | Run appropriate existing regression suites, build and browser smoke checks; update daily report with actual results | Baseline failures must not be hidden by dependency upgrades, weakened tests or financial fixes. New tests require the repository testing guidance first | Capture real commands/exit codes/test totals, screenshots where available, actual transaction values and unresolved defects | Revert only any expressly necessary setup-only change; no test deletion or bulk fixes |
| D02-08 | Update `DAILY_REPORT.md` and create `DAY_02_REPORT.md` under the standing daily-report instruction | Do not overwrite historical Day 01 evidence or claim a commit/deploy that did not happen | Use the same eight report sections and real Git references; distinguish completed, failed and blocked checks | Preserve dated reports and restore only the latest-report pointer/content if necessary |

Out of scope for Day 02: runtime rebranding, dependency upgrades, changing package identities/namespaces, modifying financial logic or migration files, touching another project's services/data, release/workflow execution, pushing commits and production changes. Existing migrations may run only on the new local disposable database. Before any necessary change not listed here, add its scope/risk/check/rollback to this amendment.

Runtime decision: the owner explicitly approved “Cho phép native cô lập cho Day 02” in this session. This authorizes native PHP/Composer/Node commands for this local Day 02 setup instead of Sail; it does not change the committed `AGENTS.md` policy for other work. Use `/opt/homebrew/opt/php/bin/php` (8.5.6), the existing Homebrew Composer, Node 26 and a separate MySQL 9.6 instance. These choices avoid global installs and satisfy the declared PHP/Node ranges, subject to real platform checks; they do not reproduce the repository's PHP 8.4 / Node 24 / MySQL 8 CI matrix.

Planned isolated paths/endpoints: ignored `storage/app/day02-local/` for Composer/npm caches, MySQL data/logs and evidence; a new ignored `.env` for this checkout; application `127.0.0.1:18080`; database `127.0.0.1:13316`, socket `/private/tmp/kenfinly-day02-mysql.sock`, MySQL X protocol disabled. Verify both ports and the socket are unused before starting. Use a `kenfinly_day02` development database and `testing` database in this separate instance, with credentials/privileges confined to them. Preserve `APP_NAME=YAFFA` for the untouched application baseline; use local file/array cache/session and log mail, with scheduler and optional external processing disabled. Initialize only the new data directory, never Homebrew's shared data directory. Pass `--no-defaults` to project MySQL commands to avoid inheriting host connection settings. Do not start a Homebrew service, edit shell profiles or change global symlinks.

Documentation consulted for the approved setup: [Laravel 13 installation](https://laravel.com/docs/13.x/installation), [Composer install](https://getcomposer.org/doc/03-cli.md#install-i), [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/) and [MySQL multiple-instance isolation](https://dev.mysql.com/doc/refman/9.6/en/multiple-servers.html). The MySQL website currently redirects its 9.6 manual URLs to 9.7; validate actual server options with the installed binary before using them.

Verification adjustment, recorded before retry: the first PHP baseline run exhausted the host CLI's 128 MiB memory limit. Retry the existing Pest runner directly with a per-process `-d memory_limit=1G`; this changes no global `php.ini` or application code, and rollback is simply omitting the invocation flag. Preserve the initial failure log. Build and all 40 existing JS tests have passed. The unchanged full translation checker reports 308 errors and 91 warnings; retain this baseline defect rather than editing locales during setup.

Browser adjustment: the in-app Browser runtime reports no available backends. Use the repository's existing Pest/Playwright browser suites for the requested UI checks, installing the locked Chromium runtime only under ignored `storage/app/day02-local/playwright/`. Do not install a system browser, extension or global Playwright package. Keep generated screenshots/evidence local; report each unexecuted manual/UI step explicitly.

After the 1 GiB PHP retry, 1,801 tests passed and five incoming-email tests failed because this smoke environment intentionally leaves `INCOMING_RECEIPTS_EMAIL` empty. Supply the synthetic receipt address used by the existing CI configuration to test processes only, with the existing array mailer; do not activate incoming mail for the development app. Rerun the affected file before repeating the full baseline. This is test-environment completion, not permission to edit tests or mail logic.

The deterministic financial fixture in D02-06 may also be exercised through the real local HTTP endpoints using an authenticated synthetic demo session, with request/response evidence under the ignored evidence directory. Use only existing account/transaction/report endpoints and Boost read-only inspection; do not create a custom financial verification script or use Tinker to mutate models. The separate existing Pest browser tests provide UI coverage; an HTTP pass is not labeled a manual visual/UI pass.

Additional local verification operation, recorded before execution: the real new-account flow stored USD 1,000/500 correctly but the balance API returned only USD 100/100 after the transactions, because neither new account had its opening-balance summary row. The existing full-recalculation job inserts that row, while incremental transaction recalculation assumes it already exists. Preserve the failing HTTP/Boost evidence and classify the initial new-account reporting gap as an unresolved baseline defect. Run only the existing `app:cache:account-monthly-summaries` command for account entities 34 and 35, summary type `account_balance`, data type `fact`, in the isolated development database; reread the same reports. This rebuild changes derived test summaries only, not transaction/account values, financial logic or schema. Rollback is unnecessary for disposable derived data, but the original responses remain retained; do not erase the defect just because the workaround succeeds. No general scheduler, full-user recalculation or production job is authorized. Capture a login screenshot with the already locked Playwright CLI as local evidence; retain the distinction between automated UI coverage and a full manual visual review.

### Day 02 execution outcome

Completed: actual Day 01 review, 211 locked Composer installs, 324 locked npm installs, platform check, local configuration, a separate native MySQL instance, original schema load plus seven pending migrations, existing demo seeding, frontend build, 1,806 Unit/Feature tests (6,427 assertions), 40 JS tests, 25 critical browser tests (387 assertions) and two additional report-filter browser tests (10 assertions). The latter file is ungrouped and was run separately because `--group=critical` did not select it. Login/health endpoints return HTTP 200, wrong-password login is rejected, and the authenticated HTTP financial fixture has been executed. After the existing summary rebuild, native USD balances are 1,100 and 600, totaling 1,700. The login screenshot was captured and visually inspected.

Remaining: fix/design review for new-account opening-summary initialization, 308 translation-check errors / 91 warnings, the full browser/Dusk suites, official Sail/CI runtime parity, actual rebranding and all release approvals. No financial logic, schema source, lockfile, package identity, production service or global runtime configuration was changed. No new commits or pushes were made. See `DAY_02_REPORT.md` for precise evidence, caveats, restart/stop instructions and follow-up decisions.

## 1. Scope and safeguards

Day 01 delivers the requested audit, specification, license review, change plan and reports, plus explicit README attribution and a local upstream Git reference. Application rebranding is proposed below, not implemented today. No financial calculations, schema, migrations, dependencies, runtime environment files or deployment configuration have been changed.

The first implementation stage covers display names, copy, titles, owned brand assets and presentation metadata. It must preserve existing financial behavior, authentication, routes, API contracts, data, package identities and operational identifiers. Do not perform a repository-wide replacement of `YAFFA`, `Yaffa`, `yaffa` or `kantorge`.

Before implementation, recheck `AGENTS.md` and `.ai/rules/index.md` if that directory becomes available. `.ai/rules` is absent at the audited baseline. Confirm installed versions through Sail and consult version-matched Boost documentation before changes that depend on framework or package behavior. Boost tools are not exposed in this session. Copy-only documentation does not depend on those APIs.

## 2. Requirement tracking

| Requirement | Day 01 outcome / remaining gate |
| --- | --- |
| Preserve MIT, notices and history | `LICENSE` unchanged; history and ancestry verified; original contributors retained in README. Preserve these in all future changes. |
| Maintain upstream reference | Added and fetched `upstream`; disabled its local push URL; durable upstream link recorded in README and audit. |
| Rebrand UI and metadata | File-level plan and acceptance criteria in this document and `BRANDING_SPEC.md`; pending implementation. |
| README attribution | Added original project, author, MIT link, upstream, baseline and downstream distinction. |
| Audit internal references first | Baseline text inventory and compatibility register in `REPOSITORY_AUDIT.md`; no internal renames authorized by this stage. |
| No blind replacement | Each change below has a bounded target and explicit exclusions. |
| No financial/schema changes | No runtime or database files modified. Enforce the same limit in the branding diff. |
| Document changes, risks and rollback | Change register and rollback runbook below. |
| Install, run and pass existing tests | Attempted Sail commands fail before execution because `vendor/bin/sail` is absent. Before/after verification remains mandatory. |
| No deployment without approval | Nothing deployed or published. Release workflows require review and explicit approval before use. |

## 3. Fork and history procedure

Verified today: the checkout was clean at the start; `HEAD`, `origin/develop` and fetched `upstream/develop` identify the same baseline. There are 1,684 reachable commits; the clone is not shallow; `git fsck --full --no-reflogs` returned success. No commits were created, amended, rebased, squashed or force-pushed.

The following local setup was executed:

```bash
git remote add upstream https://github.com/kantorge/yaffa.git
git remote set-url --push upstream DISABLED
git fetch --no-tags upstream develop
git merge-base --is-ancestor upstream/develop HEAD
```

`origin` remains `git@github.com:dieterlab969/Kenfinly-2.git`. `DISABLED` is an intentional non-remote push target. Each new clone needs the upstream setup because `.git/config` is not version-controlled. If `upstream` already exists, inspect its URLs first instead of repeating `remote add`.

Before source edits, create a dedicated local branch such as `chore/kenfinly-branding` from the recorded baseline. Keep small, separate commits for display copy, assets, and any separately reviewed delivery safeguards. Record the resulting SHAs in the next daily report. Use ordinary additive commits and merges to preserve the upstream ancestry; avoid history filtering or replacing the repository with an exported source archive.

No tags existed locally at audit time. Fetching only `develop` verifies that branch's ancestry, not preservation of every upstream branch/tag or GitHub fork-network membership. Before the first release, inventory upstream branches/tags, archive the required refs in a verified Git bundle or mirror, and confirm the hosted repository's fork relationship. Do not use `git push --mirror` against the Kenfinly repository. Do not automatically merge newer upstream changes into a branding-only change.

## 4. Proposed change register

“Planned” items may proceed in local development once their prerequisites are met. Production work, release publication, external publishing and new dependency choices still require Product Owner approval. All runtime changes remain unimplemented on Day 01.

| ID / state | Exact scope and proposed change | Risk / prerequisite | Rollback |
| --- | --- | --- | --- |
| P01 — Done | Local `.git/config`: add YAFFA upstream, fetch `develop`, disable upstream pushes. Keep `origin`. | Remote configuration is not shared by clones; fetched upstream could advance later. | If removal is requested, `git remote remove upstream` removes only this local remote and tracking refs; original commits and origin remain. Re-add from the commands above if needed. |
| P02 — Done | `README.md`: add KENFINLY identity, exact tagline, original attribution, upstream and baseline; retain inherited documentation and contributors. Create the six requested planning/report files. | Readers could mistake inherited upstream services/features for Kenfinly commitments. Intro explicitly identifies them. | Revert only the documentation change in a new commit, preserving attribution in any replacement README and retaining the reports in history. |
| P03 — Planned | Isolated development environment: install existing locked dependencies, configure disposable MySQL/test databases and local mail capture; establish untouched baseline. | Sail/vendor and Docker missing. No `.env` edits under inherited project instructions without owner involvement. Tests can recreate databases. | Stop only task-owned Sail services. Remove only confirmed disposable resources; never use volume deletion against shared data. Restore environment from its secure local snapshot if an approved setup changed it. |
| P04 — Planned | `.env.example`, `.env.ci`, `.env.dusk.ci`: review only `APP_NAME` and `MAIL_FROM_NAME` display values for `KENFINLY`. Leave other values and variable names intact. Existing installation `.env` changes belong to an operator-managed later step. | `APP_NAME` can influence framework/package defaults for sessions, cache, email, OTP labels and docs. Capture resolved values first; pin existing operational values outside the branding patch if needed. | Revert the display-value commit; operator restores the prior app/mail display values and refreshes caches through the established procedure. Do not regenerate `APP_KEY` or alter cookies/prefixes. |
| P05 — Planned | `resources/views/template/master.blade.php`: default title `KENFINLY`; retain page postfixes, CSRF, theme script and includes. Add agreed presentation metadata from the spec. | Title duplication, accidental template changes, incorrect metadata or cache behavior. | Revert the template commit and rebuild the same source revision; verify inherited title and favicon return. |
| P06 — Planned | `resources/views/template/layouts/page.blade.php`, `resources/views/auth/login.blade.php`, `resources/views/auth/two-factor-challenge.blade.php`: wordmark, alt text, tagline and brand links; preserve component structure and form behavior. | Responsive overflow; unreadable logo in dark mode; implying Kenfinly owns YAFFA's site. Product domain is undecided. | Revert the view change; restore prior asset references. Preserve upstream attribution in the footer. |
| P07 — Planned | `resources/views/auth/register.blade.php`, `resources/views/pages/dashboard.blade.php`, `resources/js/dashboard/components/Dashboard.vue`, `resources/js/user/UserSettings.vue`: update display sentences only. | English sentences also serve as translation keys; settings components contain financial/global state logic. | Revert copy and all matching translations together. No model/settings behavior is changed. |
| P08 — Planned | `resources/js/user/ApiTokenManager.vue` and displayed Google Drive translations: describe Kenfinly's UI while accurately naming the compatible YAFFA client/protocol and exact `yaffa.txt` filename. | A Kenfinly mobile client has not been established. Rewording cannot promise one; QR payloads and import marker names must remain compatible. | Revert only display sentences and corresponding translations. Keep protocol behavior untouched. |
| P09 — Planned | `lang/en.json`, `lang/fr.json`, `lang/hu.json`, `lang/pl.json`: update each selected display key/value with its caller; retain stable semantic keys and literal technical values. | Missing/fallback strings, grammar or accidental mutation of `yaffa.txt`, fixture emails or tokens. Native-language review before publication. | Revert caller and locale changes as one unit; run the existing translation check again. |
| P10 — Planned | `public/images/logo-small.png`, `public/images/favicon.ico`, `public/favicon.ico`: replace application-owned graphics using approved KENFINLY assets. Preserve existing consumed paths and expected dimensions initially. | New artwork/ownership not supplied; root favicon is currently empty; cached icons can hide changes. Vendor assets are excluded. | Restore all three assets from the baseline in a new commit, rebuild if applicable, and refresh local/browser caches. Retain prior build artifacts. |
| P11 — Planned | `app/Notifications/LoginSuccessNotification.php`, `app/Notifications/LoginFailedNotification.php`: replace subject brand prefix only. Inspect inherited mail signatures in `resources/views/emails/` through `app.name`. | Mail sender authorization is separate from display branding; changes could alter notification dispatch if patch is too broad. Use local mail capture only. | Revert subject changes; operator restores prior approved sender display name. Never change recipient routing or SMTP/DNS as part of this patch. |
| P12 — Planned | `resources/views/pages/sandbox-terms.blade.php`: update only instance identity and explicitly label upstream docs links; retain disclaimer text. | Upstream sandbox terms do not automatically define Kenfinly's legal terms. Owner review required for any new policy. | Restore prior template while retaining all license/disclaimer notices. |
| P13 — Review before change | `config/scramble.php`: consider API documentation UI title `KENFINLY API`; inspect generated docs after `APP_NAME` change. Change presentation fields only if installed package documentation supports them. | Scramble is version-specific; provider also customizes generated docs. Do not change API version, header names, schemas, access gate or servers. | Revert only presentation settings; regenerate local docs/cache with the verified command. |
| P14 — Separate prerequisite | `.github/workflows/deploy-private.yml`, `docker-build.yml`, `docker-build-contributor.yml`, `release-please.yml`; `deploy.php`: review and disable or approval-gate inherited publication/deployment before a release. Later point deployment/image publishing at approved Kenfinly targets. | Existing release-published triggers can deploy; images target YAFFA; deploy recipe clones upstream. Remote settings/secrets have not been inspected. Do not trigger these workflows. | Before any external execution, revert the proposed config change if unsuitable. After approval-gating is installed, keep that protection during application rollback; never restore unsafe automation just to roll back branding. Any real deployment rollback needs separate approval. |
| P15 — Planned | Existing tests: run unchanged first. Adjust only assertions that intentionally depend on new visible branding, if any; retain all financial/security assertions. No new framework or wholesale test rewrite. | Baseline failures must be recorded separately, never hidden as branding regressions. Read the project testing-best-practices skill before writing tests. | Revert only necessary assertion edits together with the corresponding display change. |
| P16 — Deferred | Namespaces, package names, config keys, API/mobile identifiers, storage/cache keys, Docker services/volumes, fixture identities and version numbering. | Compatibility and data loss risk. Requires a separate dependency audit, compatibility design, tests and owner scope decision. | No change in the initial stage, so no migration or data rollback is required. Any later proposal must supply its own tested rollback. |

## 5. Explicit exclusions

- Preserve `LICENSE` byte-for-byte and retain source/vendor notices, `CHANGELOG.md`, `UPGRADE.md` and historical authorship.
- Keep PHP namespace `App\`, the `YaffaCurrency` alias, Composer root identity `kantorge/yaffa`, dependency vendor names, package lockfiles and all dependency versions.
- Keep `config/yaffa.php`, `yaffa.*`, `window.YAFFA`, `X-Yaffa-Token`, `yaffa_version`, `yaffa://pair`, existing OTP secret/enrollment behavior, route names and API paths/payloads.
- Keep `yaffa-color-mode`, `yaffa:colorModeChange`, session-storage `YAFFA`, report cache keys, cookie names, Redis/cache prefixes and `yaffa.txt` / temporary Drive filenames.
- Keep all database names, tables, columns, precision, casts, migrations and seed/factory fixture identities. A fresh install may execute existing migrations only in a new disposable database; that is not permission to alter an existing database or write a migration.
- Do not alter transaction amounts, currency conversion, investment returns, recurring schedules, forecasts, date ranges, timezone, rounding or number/locale formatting.
- Do not edit `.env`, rotate keys, change mail domains, migrate live data, publish images, create a release or deploy under this plan without the applicable separate authorization.

## 6. Verification gates

### Gate A — Untouched baseline, before UI edits

Unblock Docker and the locked Sail bootstrap first. Do not bypass Sail with host PHP/Composer/Node. A clean machine cannot run the repository's Sail wrapper until the locked Composer dependencies have been bootstrapped; agree on the approved Sail-based bootstrap with the environment owner instead of inventing a host-tool workaround. Do not run `composer update`, `npm update` or change lockfiles.

The environment owner supplies a disposable `.env`, MySQL 8 database and separate `testing` database. Verify resolved targets with configuration/schema tools before tests. Ensure no real financial data, real mail recipients or active external import/AI credentials are present. Keep scheduler/automatic processing disabled for smoke tests. `composer run setup`, the production Docker entrypoint, demo resets and `migrate:fresh` are unsuitable shortcuts because they can run migrations or reset data.

Once Sail is available, run the following sequentially where one step depends on the previous one, retaining exit codes and output in the daily report:

```bash
vendor/bin/sail up -d
vendor/bin/sail composer install --no-interaction --prefer-dist
vendor/bin/sail composer show --direct
vendor/bin/sail composer check-platform-reqs
vendor/bin/sail npm ci
vendor/bin/sail npm run build
vendor/bin/sail artisan --version
vendor/bin/sail artisan route:list --except-vendor --no-interaction
vendor/bin/sail artisan test --compact
vendor/bin/sail npm run test:js
vendor/bin/sail php .github/scripts/check-translations.php
vendor/bin/sail npx playwright install chromium
vendor/bin/sail php vendor/bin/pest --testsuite=Browser
```

Discover command availability/options on the installed application before use. Existing `phpunit.xml` defaults to Unit + Feature; it does not include Pest Browser or legacy Dusk. Review Dusk's separate environment/DB reset behavior and then run the existing legacy suite with `vendor/bin/sail artisan dusk --no-interaction` in a dedicated disposable setup. Preserve test databases and seeded identities expected by each suite. Record baseline defects without changing their assertions to make them pass.

### Gate B — Rebranded candidate

Run the same locked install, build, Unit/Feature, JS, translation, Pest Browser and Dusk checks against the candidate in the same isolated environment. Add targeted tests only when they provide meaningful coverage; presentation-only edits do not require new tests. For any PHP edit run required Pint formatting (`vendor/bin/sail bin pint --dirty --format agent`) and the repository's existing PHPStan check. Repeat affected tests after any test edit. Review the diff for unintended formatter changes.

Capture baseline and candidate screenshots for login, registration, password reset, 2FA, desktop/mobile navigation, dashboard/onboarding, profile/settings, API token pairing, sandbox terms, a representative report and local notification emails. Cover light/dark modes and all four existing languages. Check browser titles, logo/alt text, favicon requests, descriptions and API docs title. Do not capture tokens, QR secrets or personal data in artifacts.

Use Boost `get-absolute-url` before sharing a project URL and recent `browser-logs` if available. If unavailable, record the tooling gap; do not invent a working URL or a screenshot. The original YAFFA sandbox is not evidence that this clone runs.

### Gate C — Compatibility and data invariants

Require a clean diff for `database/`, `app/Casts/`, financial models/services, financial JS helpers, lockfiles and API contracts except explicitly approved display-only files. Compare the isolated database schema before/after; no new migration or structural difference is allowed. Compare balances, transactions, budgets, currency-rate displays, forecasts and investment returns on identical test fixtures. Verify authentication, 2FA, existing cookies/preferences, token header, pairing payload and API decimal-string responses still work. Test the `APP_NAME` change against resolved cookie/cache/OTP defaults rather than assuming it is cosmetic.

### Gate D — Release approval

Require Gates A–C evidence, original license/notice verification, approved artwork/domain/sender details, a protected release workflow and an exercised local rollback. Give the Product Owner a concrete reviewed diff, commit SHA and test results. Deployment, registry push and production configuration/data changes require explicit approval. No release is approved by this document.

## 7. Rollback runbook

1. Record the candidate commit(s), prior verified source/build, lockfile hashes and local environment snapshot before implementation. Never store secrets in these reports or Git.
2. If a display regression, test regression, license omission, API change or unexpected database difference appears, stop progression to release. Keep the evidence and identify the smallest responsible commit.
3. For committed changes, use `git revert <branding-commit-sha>` in reverse dependency order on the working branch. Keep rollback additive; do not reset shared history, force-push or discard unrelated edits. For uncommitted changes, review and reverse only the task's own patch.
4. Restore the prior asset set together with its matching view/translation revision. Rebuild through Sail using the unchanged lockfiles. Refresh only the relevant development caches after verifying command availability. An operator restores display environment values only if a separate authorized change occurred.
5. Rerun affected checks and the same smoke journeys. Confirm the unchanged license hash and critical-file diff. No schema down-migration, database restore, key rotation or volume deletion should be needed for branding. If one appears necessary, the patch exceeded scope and must be investigated.
6. A future production rollback, if ever needed, is a separate approval-controlled operation using the previously verified release artifact. Do not execute it as part of Day 01 or automatically re-enable inherited deployment workflows.

## 8. Day 01 exit decision (historical)

Safe to continue environment setup and review the proposed branding. Not yet verified safe to merge runtime branding or release. The six requested planning/report documents and README attribution are prepared; installation, runtime, screenshots, tests and rollback rehearsal remain open gates. See `DAY_01_REPORT.md` for actual command outcomes.
