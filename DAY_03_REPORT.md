# KENFINLY 2.0 — Daily Engineering Report

Date: 2026-11-18 (Asia/Ho_Chi_Minh)\
Day: 03\
Objective: Execute isolated local HTTPS development at alpha.my.kenfinly.com and document reproducible onboarding with measured evidence.\
Status: Completed

The local environment works within the scope verified below. Existing opening-summary and translation defects remain open. This is not release approval or a completed UI rebrand.

## 1. Completed Work

- Reviewed actual Day 01/02 documents, instructions, Git state, source, lockfiles, environment examples and installed services before changing configuration. Added the Day 03 scope/reason/risk/verification/rollback register to `CHANGE_PLAN.md` first.
- Reused the owner-authorized isolated native approach and existing Apple Silicon tooling; did not install Docker, relink PHP/Node or alter the Sail policy. Confirmed installed PHP 8.5.6, Composer 2.10.0, Node 26.0.0, npm 11.12.1, MySQL 9.6.0 and repository package versions.
- Added repeatable project service/setup helpers in `kenfinly-local` and `docker/local/`, with ownership/conflict checks, private backups, local DB identity checks and safe start/stop behavior.
- Configured the required loopback hostname, a new certificate from the existing trusted mkcert CA, one Nginx site and a separate project FPM pool. The owner completed the reviewed hosts/reload administrator helpers. Existing sites/configuration and shared services were preserved.
- Configured the local HTTPS app/assets origin, a uniquely named host-only Secure/HttpOnly session, exact Sanctum hostname, local mail catcher, database worker and scheduler. Preserved the existing application key and isolated Day 02 development/test data.
- Verified real registration/login, CSRF rejection, cookie isolation, wallet/income/expense persistence, queued summary processing, app restart, local password-reset email, asset delivery and a live WSS hot update. The known opening-summary workaround remains explicit.
- Ran the existing PHP/JS suite and build successfully. Tested production/foreign-state refusal, repeated setup/start and fresh database initialization/migrations in separate scratch data. Restored the original database and checked unchanged row counts. Retired the superseded owned Day 02 HTTP server on port 18080.
- Created English onboarding and verification documents. Measured actual provisioned-Mac operations without claiming a fresh Mac/clone is verified in 15 minutes.

Git reference: `develop`, `e3936669c7906550024f56e61aca80cf0d834da8`. No new commit, push, release, hosted workflow or deployment. The setup changes remain reviewable working-tree files; Day 01/02 reports remain byte-identical.

## 2. Deliverables

| Path | Output |
| --- | --- |
| `docs/ONBOARDING.md` | English prerequisites, exact tested versions, clone/ref boundary, locked install, local configuration/DB/TLS, services, verification, troubleshooting, safe reset/rollback and timings |
| `docs/LOCAL_VERIFICATION.md` | Actual configuration, commands/results, private evidence locations, measurements, failure corrections and remaining limits |
| `CHANGE_PLAN.md` | Day 03 implementation register, trust-store/scratch-verification adjustments and execution outcome |
| `kenfinly-local` | Standard-library Python command entry point for owned project services/setup/tests |
| `docker/local/hostname.sh`, `activate.sh` | Minimal reviewed administrator hosts and checked Nginx graceful reload helpers |
| `docker/local/php-fpm.conf.template`, `nginx.conf.template` | Separate FPM pool and exact-host HTTPS site configuration |
| `docker/local/vite.config.mjs` | Loopback HTTPS/WSS development wrapper preserving base Vite configuration |
| `docker/local/verify.mjs` | Opt-in synthetic HTTPS/HMR/mail/restart infrastructure check using locked Playwright |
| `DAY_03_REPORT.md`, `DAILY_REPORT.md` | Dated report and identical current daily report |
| `README.md` | Links to current onboarding, verification and Day 03 report; original attribution retained |
| Ignored `.env`, `storage/app/kenfinly-local/` | Local credentials/config backups, leaf certificate, process state/logs, mail database, caches, screenshots and measured evidence |

No credentials, cookies, CA private key, database contents or TLS private keys are included in distributable source files.

## 3. Verification

| Command/check | Result |
| --- | --- |
| `./kenfinly-local setup --adopt-existing-env` | Exit 0, **27.22s** on the existing provisioned checkout; original key/data retained |
| Locked Composer install/platform check/package discovery | Exit 0, no dependency updates |
| `npm ci` and `npm run build` through the helper | Exit 0; 324 locked JS packages; existing build notices retained |
| Normal TLS curl `/login` and `/up`; macOS certificate verification | HTTP **200**, TLS result **0**; no bypass |
| Real Chromium via `./kenfinly-local verify` | Exit 0, **12.86s**; TLS 1.3, registration/login, wrong-password rejection, CSRF 419, secure host-only cookie, no cookie selected for production hostname |
| Synthetic financial endpoint flow | Wallet opening USD 500, income 150, expense 30; existing full-summary rebuild produces **620**; five queued jobs observed before worker resumes |
| Restart/mail/HMR | Data/session retained, local reset email captured, HTTPS dev assets/WSS and actual **initial → updated** hot update pass; built mode restored |
| `./kenfinly-local test` | **1,806 PHP tests passed / 6,427 assertions**, **40 JS tests passed**, total **74.04s** |
| Fresh scratch database provisioning/migration | Pass, **3.331s + 0.839s**, 0 users; original instance restored |
| Retained development data | **48 users, 114 transactions, 43 account entities** before/after restoration/repeated setup; original key unchanged |
| Repeated setup and start | **19.77s** + **0.38s**; no Nginx site change or new reload, repeated `up` preserves PIDs |
| Safety guards / syntax | Existing/production env and foreign state refused without env overwrite; shell/Python/Node syntax checks pass |
| Isolation/preservation | Non-loopback HTTPS returns **403**; shared configuration hashes and service processes preserved; four other local sites respond |
| Protected files | MIT license, both lockfiles, Day 01/02 archives unchanged; no application financial/schema/test source modification |

Raw evidence is under ignored `storage/app/kenfinly-local/evidence/`, with detailed command/stage logs and `timings.jsonl` in its parent. Screenshots `wallet-https.png`, `wallet-history-https.png` and `dashboard-https.png` were visually inspected; they still show inherited YAFFA branding. `docs/LOCAL_VERIFICATION.md` distinguishes browser interaction from authenticated endpoint verification and records initial diagnostic failures.

The fresh schema has 105 historical migration records; 61 migration source files are present. Day 02's status-list wording was imprecise; the dated report is retained, and no schema source was changed.

## 4. Issues and Risks

- **D02-F01:** fresh-account derived summaries can omit opening balance until the existing full-summary operation runs. Preserved as a baseline defect; no financial formula/schema correction included.
- Existing translation checker baseline: **308 errors, 91 warnings**. Not fixed or represented as a passing check.
- Tested native runtime differs from official Sail/CI. Full browser/Dusk, manual Safari, mobile/dark mode, nightly jobs and optional external integrations remain unverified.
- Fifteen-minute onboarding is a conditional goal for a provisioned Mac. Cold downloads, fresh trust/tool installation, remote clone/ref publication and administrator time were not measured. No fresh-Mac claim is supported.
- Helpers/docs are uncommitted and unpublished. A reviewed setup ref must be available before another developer can follow remote-clone onboarding.
- UI remains YAFFA in many places; display rebranding, dependency distribution review, inherited release automation and production hardening remain separate work.

## 5. Changes Made

Project-local changes: ignored `.env` updated to the HTTPS/local service profile after backup; original APP_KEY retained. Existing dedicated database/credentials reused without reset. Added owned FPM, SMTP/catcher, queue/scheduler and opt-in Vite processes; private state stays under ignored storage. Reinstalled locked JS dependencies and regenerated build assets; reused Composer packages and local Chromium. No dependency version changes or global runtime installation.

Host integration: one marked loopback hosts block, one new Nginx site and leaf certificate from the already trusted local CA. The owner performed administrator activation. Shared Nginx was gracefully reloaded; its original master and all other configurations/services were preserved. No public DNS, production secret/database or Ubuntu configuration was used.

Start/stop from the checkout:

```bash
./kenfinly-local up
./kenfinly-local status
./kenfinly-local dev start   # optional
./kenfinly-local dev stop
./kenfinly-local down       # keeps the database/data
./kenfinly-local down --database  # also stops only the owned DB
```

Working URL: **https://alpha.my.kenfinly.com**. Local mail UI: `http://127.0.0.1:18025`. Services are left running in built-asset mode; no boot/login autostart was installed. Reset is never part of routine setup/start. Follow the explicitly destructive local-only procedure in onboarding only when intended.

## 6. Decisions Required

- Review/publish the prepared setup change set before inviting another developer to clone it.
- Approve a separate focused correction/regression scope for D02-F01, and prioritize translation repairs separately.
- Select the continuing team runtime policy: this measured native profile or official Sail/CI parity for subsequent engineering.
- Approve brand assets/display-rebranding scope and any future release/deployment separately. No approval is needed to use the currently prepared local site.

## 7. Next-Day Plan

1. Review and publish the setup branch; run the onboarding guide from a clean checkout on a second provisioned Apple Silicon Mac and measure the entire sequence, including download/admin boundaries.
2. Reproduce and scope D02-F01 with a meaningful regression test before changing account-summary behavior; preserve financial formulas/schema constraints.
3. Agree the runtime matrix and run corresponding CI/Sail checks; complete remaining browser coverage where required.
4. Address translations in a bounded follow-up, then resume approved display branding with MIT/history/upstream safeguards.
5. Continue the same dated daily-report format, archiving this report. No unattended daily automation was created.

## 8. Release Readiness

**Ready for continued isolated local development.** Trusted HTTPS, registration/login, local session isolation, real account/transaction endpoints, restart persistence, background processing, mail capture, HMR, build and existing PHP/JS tests have executed evidence. The original data/key and unrelated projects are preserved.

**Not ready for production or a release.** The initial account-summary defect and translation failures remain, complete onboarding on another Mac and official runtime/full browser parity are unverified, runtime UI branding is incomplete, and setup publication/release review remain pending. No deployment or production change was performed.
