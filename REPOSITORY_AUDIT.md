# KENFINLY 2.0 — YAFFA Repository Audit

Date: 2026-11-16 (Asia/Ho_Chi_Minh)\
Audited commit: `e3936669c7906550024f56e61aca80cf0d834da8`\
Scope: Git provenance, architecture, branding references, dependency metadata and verification readiness. This is a static audit, not a certification of financial correctness or security.

## Day 02 review supplement — 2026-11-17

The sections below retain the Day 01 audit. The following facts were independently rechecked against actual files, Git, runtime and HTTP/test results on Day 02; proposals in the original plan were not treated as completed work.

| Item | Actual Day 02 finding |
| --- | --- |
| Requested Day 01 documents | All five present, plus `DAILY_REPORT.md`; none missing. At the start all six were untracked. README was modified but uncommitted |
| Actual implementation commits | None since `e3936669c7906550024f56e61aca80cf0d834da8`; `develop`, origin tracking and existing upstream tracking ref retain that baseline |
| History/license | 1,684 commits, Git integrity check successful, original MIT hash unchanged; upstream push URL still `DISABLED` |
| Application rebranding | Not implemented; source title/wordmark and the inspected live screenshot still show YAFFA |
| Reference index | Reproduced the pinned 274 files / 1,220 matching lines; matches the appendix |
| New actual local setup | Owner-approved Day 02 native exception to Sail; Homebrew PHP 8.5.6, Composer 2.10.0, Node 26.0.0, npm 11.12.1, a separate MySQL 9.6.0 instance on 127.0.0.1:13316. Existing host services remain running |
| Dependency installation | 211 Composer and 324 npm packages installed from unchanged lockfiles; PHP platform check passed |
| Local database/application | Original schema dump + seven migrations applied only to new `kenfinly_day02`; separate `testing` DB in the same isolated instance. App login/health return HTTP 200 at the Boost-resolved local address |
| Boost access | Directly registered MCP tools remain absent in this session, but the installed Boost 2.10.4 CLI `boost:execute-tool` now exposes its real read-only schema/query and URL tools; those were used. Boost is disabled under `APP_ENV=testing`, so test-target inspection used local Boost with explicit test DB credentials |
| Regression results | Build, platform check, 1,806 Unit/Feature tests, 40 JS tests and 27 focused browser tests passed. Full browser/Dusk suites were not run |
| Actual financial-flow check | Real authenticated HTTP account/income/expense/transfer/edit requests succeeded. The initial balance report omitted new-account opening balances; targeted existing full-summary rebuild produced USD 1,100 / 600, total 1,700. Initial failure remains an unresolved defect, not a clean onboarding pass |
| Translation checker | Existing full checker fails with 308 errors and 91 warnings; no locale files were changed |
| Day 01 report preservation | `DAY_01_REPORT.md` retained unchanged, SHA-256 `c5076e01bbb353777ab66d0dd3b906d36eeef41d05c89a509519b9660ab5d596` |

The initial setup blockers described in Day 01 are historical. Day 02 used an explicitly approved native environment; it does not prove parity with PHP 8.4 / Node 24 / MySQL 8 in Sail/CI. Read [DAY_02_REPORT.md](DAY_02_REPORT.md) for commands, actual results and remaining limitations. The successful test suites do not override the new-account summary issue found through the separate real HTTP scenario.

## 1. Repository provenance

| Item | Evidence |
| --- | --- |
| Local checkout | `/Users/dieter/Projects/Kenfinly-2` |
| Current branch | `develop`, tracking `origin/develop` |
| Original project | [kantorge/yaffa](https://github.com/kantorge/yaffa) |
| Kenfinly origin | `git@github.com:dieterlab969/Kenfinly-2.git` |
| Upstream remote | Added `https://github.com/kantorge/yaffa.git`; local push URL `DISABLED` |
| Fetched source branch | `upstream/develop`, identical to local `HEAD` at audit time |
| Latest baseline commit | `e3936669` — `fix: transaction form mobile layout and behavior`, 2026-11-13 |
| Reachable history | 1,684 commits; `git rev-parse --is-shallow-repository` returned `false` |
| Root commit | `bc19d491cb284ad8ee8189a8d33c17df20f0eb56` — `first commit`, 2020-09-21 |
| Git object integrity | `git fsck --full --no-reflogs` exited 0 |
| Local tags | None at audit time; only upstream `develop` was fetched, without tags |
| Starting worktree | Clean before this task |

`git merge-base --is-ancestor upstream/develop HEAD` succeeded and both refs resolve to the same full SHA. This proves the audited branch ancestry and starting tree, not the GitHub fork-network relationship or a mirror of all upstream refs. No history rewriting, commits, pushes or releases were performed.

The original project license is MIT, with `Copyright (c) 2021 Gergely Kántor`. The file and original contributor credit are retained; see [LICENSE_REVIEW.md](LICENSE_REVIEW.md).

## 2. Instructions and tooling

`AGENTS.md` was read. `.ai/rules` and its index do not exist in this checkout, so no matching rule files or keyword grep were available. Existing root `CLAUDE.md`, `tests/CLAUDE.md`, domain/UI context, README, upgrade notes, manifests and relevant source/config/workflows were consulted. An older `.github/copilot-instructions.md` says Laravel 12; lock metadata and root context indicate Laravel 13. Resolve such discrepancies using the installed packages before implementing API-dependent changes.

Laravel Boost tools (`search-docs`, `database-schema`, `get-absolute-url`, `browser-logs`) are not exposed in this session. No live database was queried, no schema was inspected through an application connection, and no running application URL is asserted. Filesystem/Git inspection was used for this document-only stage.

The application requires Sail for PHP, Artisan, Composer and Node commands. `vendor`, `node_modules`, `.env` and `vendor/bin/sail` are absent. `command -v docker` found no Docker CLI on PATH. This blocks establishing installed versions and exercising the application in this session. No host PHP/Composer/Node workaround was used.

## 3. Architecture and protected behavior

| Area | Evidence / implication for branding |
| --- | --- |
| Server | Laravel MVC with `app/Http/Controllers`, Form Requests, Resources, services, models, casts and policies; keep PHP `App\` namespace |
| UI | Blade multi-page layouts and Vue 3 islands; shared shell is `resources/views/template/master.blade.php` and `template/layouts/page.blade.php` |
| Frontend | Vite build, Bootstrap/CoreUI, charts and jQuery/DataTables integrations; rebuild after actual JS/Vue/SCSS edits |
| Financial precision | `app/Casts/MoneyCast.php`, `DecimalCast.php`, Brick Money/Math; financial API values include decimal strings. Do not change casts, wire types or formatting while renaming display text |
| Transactions/budgets | `app/Services/TransactionService.php`, `TransactionCreationService.php`, `BudgetService.php`, financial models and controllers; protected from branding edits |
| Forecast/recurrence | `RecurrenceRuleService.php`, `InflationCalculator.php`, model recurrence concerns and report JS; preserve RRULE handling, dates and calculations |
| Investments/currency | `InvestmentService.php`, `CurrencyService.php`, `CurrencyRateService.php`, `resources/js/investments/lib/investmentReturn.js`, `resources/js/shared/lib/money/scale.js`; no logic edits |
| Persistence | Existing `database/migrations`, factories and seeders. MySQL 8 is configured in Docker; live schema/data have not been inspected |
| Async/integrations | Queues/scheduler, incoming email, Google Drive, optional AI/OCR and price providers. Display rebranding must not activate these or change recipients/credentials |
| Authentication/API | Sanctum tokens, 2FA, device pairing, existing web/API routes; protect headers, URL schemes, abilities, gates and OTP behavior |

The root `docker-compose.yml` is the Sail development stack (`yaffa.test`, `mysql`, MailHog, Selenium). `docker/docker-compose.yml` is a separate distribution stack with persistent YAFFA-named volumes, an app, scheduler and Redis. Do not interchange their environment assumptions.

## 4. Versions: declared versus locked versus installed

Installed versions remain **unverified**. `vendor/bin/sail composer show --direct` failed because Sail is missing. The table records only checked-in manifests and lockfiles.

| Package/runtime | Declared configuration | Locked metadata |
| --- | --- | --- |
| PHP | `^8.4`; Sail runtime 8.4; image PHP 8.4 | Host/container runtime unverified |
| Laravel framework | `^13.34` | `v13.40.0` |
| Laravel Sail | `^1.53` | `v1.69.0` |
| Laravel UI | `^4.6` | `v4.6.3` |
| Pest | `^5.2` | `v5.3.5` |
| PHPUnit | `^13.0` | `13.4.5` |
| Prism | `^0.100` | `v0.100.1` |
| Brick Money / Math | `^0.14` / `^0.20` | `0.14.2` / `0.20.0` |
| Node | CI and Docker use 24 | Local/Sail version unverified |
| Vue | `^3.5.43` | `3.5.45` |
| Vite | `^8.3.5` | `8.3.6` |
| Playwright | `^1.65.0` | `1.65.0` |
| amCharts 4 | `^4.10.40` | `4.10.40` |

The upstream Composer project version is `4.0.0`. Kenfinly 2.0 is a product designation; no software/API release-number change is implied. The root npm package has `private: true` and no `name` field, so there is no root npm YAFFA name to replace. Do not rename nested JS module package files merely because they are called `package.json`.

## 5. Reference inventory method

The pinned tracked-text scan found **274 files with 1,220 matching lines** for the combined case-insensitive pattern `yaffa|yet another free financial|kantorge`. Matching lines are not individual string occurrences. The appendix lists every matching tracked file and its matching-line count. Binary assets were inspected separately by path/type.

| Area | Matching files | Matching lines | Initial disposition |
| --- | ---: | ---: | --- |
| Root files | 15 | 457 | README attribution; preserve manifests, historical docs and operational identities |
| `.ai` | 61 | 197 | Preserve inherited domain/specification context; not user-facing branding |
| `.github` | 7 | 11 | Review release/deployment ownership; preserve dependency/fixture references |
| `app` | 32 | 68 | Only two notification subject prefixes are initial display targets; keep internal references |
| `config` | 2 | 2 | Keep config keys/file names and timezone behavior |
| `database` | 3 | 4 | Preserve seed/factory identities; no migration rename or schema edit |
| `docker` | 1 | 26 | Preserve persistent resource names and image variable until separate delivery review |
| `lang` | 4 | 81 | Review individual display keys/values; retain technical literals |
| `resources` | 98 | 253 | Separate UI text/assets from JS globals, storage, events and calculations |
| `routes` | 1 | 3 | Keep scheduler config contract |
| `tests` | 50 | 118 | Keep fixtures/config/protocol assertions; only intentional display expectations may change later |
| Total | 274 | 1,220 | No blanket replacement |

Reproduce the original inventory even after documents or UI change:

```bash
git grep -I -i -n -E 'yaffa|yet another free financial|kantorge' e3936669c7906550024f56e61aca80cf0d834da8
git grep -I -i -c -E 'yaffa|yet another free financial|kantorge' e3936669c7906550024f56e61aca80cf0d834da8
git ls-files '*[Yy][Aa][Ff][Ff][Aa]*' '*[Ll][Oo][Gg][Oo]*' '*[Ff][Aa][Vv][Ii][Cc][Oo][Nn]*'
```

The working-tree reconnaissance used `rg` first, including hidden tracked areas while excluding `.git`, dependencies and generated runtime/build files. The pinned Git scan avoids accidentally counting the new audit documents. This inventory does not prove that binaries, remote services, secrets, live database contents or generated dependencies contain no other references. Any later internal rename requires consumer-by-consumer analysis and compatibility tests; this document does not authorize one.

## 6. Display reference map

| Surface | Exact locations | Decision |
| --- | --- | --- |
| Browser title/favicon/meta | `resources/views/template/master.blade.php` | Plan KENFINLY title, reviewed metadata and new owned favicon; keep theme/storage/CSRF/Vite behavior |
| Sidebar/header/footer | `resources/views/template/layouts/page.blade.php` | Rebrand display identity and alt text; separate product link from upstream credit |
| Authentication/registration | `resources/views/auth/login.blade.php`, `two-factor-challenge.blade.php`, `register.blade.php` | Update brand copy without form/route/2FA changes |
| Dashboard/onboarding | `resources/views/pages/dashboard.blade.php`, `resources/js/dashboard/components/Dashboard.vue` | Copy-only changes with all translations |
| Settings/token manager | `resources/js/user/UserSettings.vue`, `ApiTokenManager.vue` | Display copy only; accurately describe the existing YAFFA client and API compatibility |
| Drive instructions | `lang/{en,fr,hu,pl}.json`, `resources/js/user/GoogleDriveSettings.vue` | Display names can change; exact `yaffa.txt` remains |
| Translations | `lang/en.json`, `fr.json`, `hu.json`, `pl.json` | English literals are keys; update selected callers and language files together |
| Emails | Two login notification subjects under `app/Notifications/`; signatures under `resources/views/emails/` use `app.name` | Prefix/display review only; preserve SMTP, recipient and event logic |
| Sandbox/legal text | `resources/views/pages/sandbox-terms.blade.php` | Identify the appropriate test instance; retain disclaimer and upstream docs distinction |
| Logos/icons | `public/images/logo-small.png` (44×44), `public/images/favicon.ico` (32×32), empty `public/favicon.ico` | New approved artwork pending; vendor assets excluded |
| Public metadata | Shared head has no app description, OG/Twitter cards, web app manifest or Apple touch icon | Add only approved description/application-name initially; no invented domain or social image |

## 7. Internal compatibility register

| Reference | Producer / consumers | Risk if blindly renamed / disposition |
| --- | --- | --- |
| PHP `App\` | Composer PSR-4 autoload, application classes/tests | This is already generic; renaming breaks autoload and adds needless churn. Keep |
| `YaffaCurrency` | `app/Casts/MoneyCast.php` alias of `App\Models\Currency` | Financial cast code, not display branding. Keep |
| `kantorge/yaffa` | Composer root package and lock metadata | Package/tooling/history identity. Keep during initial branding |
| `kantorge/laravel-currency-exchange-rates`, `Kantorge\CurrencyExchangeRates` | Composer dependency and `app/Models/Currency.php` | Real third-party package/namespace; renaming would break currency retrieval. Keep |
| `github:kantorge/datatables-contextual-actions#custom_package` | `package.json` and lockfile | Real dependency source. Keep |
| `yaffa.*` / `config/yaffa.php` | Config consumed by controllers, requests, listeners, providers, commands, schedules, views and tests | Authentication, scheduler, imports, limits, sandbox and admin routing depend on it. Keep |
| `YAFFA` / `window.YAFFA` | `JavaScriptVariablesComposer.php` payload consumed across `resources/js/`, locale/format/chart/form components and tests | Changing only one side breaks pages and can affect rendered financial values. Keep |
| `yaffa-color-mode`, `yaffa:colorModeChange` | Master head, `shared/lib/ui/colorMode.js`, `amchartsColorTheme.js` | Stored preferences and chart listeners must agree. Keep |
| Session-storage `YAFFA` | `shared/lib/ui/sidebarVisibilityPersistence.js` | Losing existing UI state; key is not the displayed wordmark. Keep |
| `yaffa_transactions_cache`, `yaffa_breakdown_cache` | `reports/components/find-transactions/FindTransactions.vue` | Report caching/state compatibility. Keep |
| `X-Yaffa-Token` | `AppServiceProvider.php`, `MetaApiController.php`, API docs/tests | Changing it breaks existing authentication clients. Keep |
| `yaffa://pair` | `ApiTokenService.php`, token API controller, mobile pairing consumers/tests | Deep-link protocol/QR payload, not UI copy. Keep |
| `yaffa_version` | `MetaApiController.php`, version metadata and tests | Existing response contract. Keep |
| `APP_NAME` / `MAIL_FROM_NAME` | Environment templates, framework defaults, mail signatures, docs and potentially OTP | Display candidate with indirect behavior risk. Inspect resolved cookies, cache prefixes, OTP labels and mail behavior before changing values |
| `OTP_TOTP_ISSUER` | `config/two-factor.php`; installed package defaults not inspected | Existing enrollments must remain usable. Do not rename issuer/secrets or force reenrollment under branding |
| DB names/users, `CACHE_PREFIX`, `SESSION_COOKIE`, `REDIS_PREFIX` | `.env.example`, `.env.ci`, `.env.dusk.ci`, runtime defaults | Could disconnect data, invalidate sessions or lose cache isolation. Keep |
| `APP_SERVICE=yaffa.test` | Env templates and root Compose service | Sail command target. Renaming one side breaks development. Keep |
| `YAFFA_IMAGE`, `yaffa_db`, `yaffa_storage`, `yaffa-network`, `yaffa_*` containers | `docker/docker-compose.yml` | New volumes can look like lost data; image defaults still pull upstream. No changes in first display patch |
| `yaffa.txt`, `yaffa_cap_*` | `GoogleDriveService.php`, translations and Drive tests | Capability/exclusion behavior depends on exact filenames. Keep |
| `_yaffa_` MIME boundary | `SimulateIncomingEmail.php` | Internal generated marker. No display benefit to changing it |
| `demo@yaffa.cc`, `other@yaffa.cc`, test/admin/receipt domains | Seeders, factories, reset commands, sandbox helper, data layer listeners and tests | Cross-linked fixture identities, routes and analytics conditions. Keep; never send real mail as part of verification |
| `yaffa.gtm_container_id` | Sandbox head/body includes and event listeners | Analytics config and sandbox behavior. Keep; do not introduce new tracking |
| `yaffa` Deployer task / upstream repository URL | `deploy.php`, `.github/workflows/deploy-private.yml` | Can deploy the wrong codebase/target. Separate approval-controlled delivery review |
| Upstream docs/changelog/context | README, `CHANGELOG.md`, `UPGRADE.md`, `.ai/**`, `CLAUDE.md` | Historical references and authorship, not stale branding to erase |

No matching text was found under the tracked `database/migrations` or `database/schema` paths using the inventory pattern. This says nothing about a live database and is not a reason to rename tables, fields, foreign keys or migration files. Branding does not require schema changes.

## 8. Release and environment findings

| Finding | Evidence / consequence | Action |
| --- | --- | --- |
| Automatic inherited deploy | `.github/workflows/deploy-private.yml` runs on a published release and manual dispatch; uses Private/Sandbox environments | Review and disable or approval-gate before any release. No workflow triggered today |
| Wrong deployment source for a fork | `deploy.php` still clones `https://github.com/kantorge/yaffa.git` and defaults to `main` | Separate reviewed delivery change before deploying Kenfinly |
| Upstream image publishing targets | `docker-build.yml` pushes `kantorge/yaffa` on release/manual dispatch; contributor build can push GHCR images | Do not run; require owned destinations and approval before publication |
| Release automation | `release-please.yml` runs on pushes to `main` | Inspect hosted Actions settings and credentials before pushing release-sensitive refs; no hosted settings were inspected |
| Production container performs writes on boot | `docker/entrypoint.sh` runs existing migrations with `--force`, syncs import profiles and optimizes; scheduler can process jobs | Do not use it against a real DB for smoke tests. Inspect/contain test entrypoint effects |
| Setup command performs writes | Composer `setup` includes key generation, migration and npm install | Avoid using it as a harmless health check |
| Environment templates target different contexts | Example DB host defaults to `127.0.0.1`; root Sail DB service is `mysql`; CI templates assume host-based MySQL; test DB/credentials differ from example | Owner-managed disposable Sail/test environment must reconcile this before running tests; do not simply copy CI values into a live environment |
| Inherited `.env` rule | Root `CLAUDE.md` marks `.env` off-limits without owner involvement | No `.env` created or edited today |
| Missing local runtime | No Docker CLI on PATH, Sail/vendor, npm install or `.env` | Baseline install/run/tests blocked |
| Asset/license inputs missing | No approved KENFINLY artwork; dependency license metadata includes special and missing entries | Follow `LICENSE_REVIEW.md`; no claim of blanket MIT coverage |

## 9. Existing verification coverage

| Suite/check | Checked-in evidence | Day 01 result |
| --- | --- | --- |
| Unit | 59 `*Test.php` files in `tests/Unit` | Not executed |
| Feature | 140 `*Test.php` files in `tests/Feature` | Not executed |
| Pest Browser | 23 `*Test.php` files in `tests/PEST`; Browser suite in `phpunit.xml` | Not executed |
| Legacy Dusk | 22 `*Test.php` files in `tests/Browser` | Not executed |
| JS | Four colocated `*.test.js` files; `npm run test:js` | Command blocked before test runner |
| Build | `npm run build` uses Vite | Command blocked before Vite |
| Translation synchronization | `.github/scripts/check-translations.php` | Inspected; not executed |
| Existing CI | Unit, Feature, JS, E2E, Dusk, Pint, PHPStan, translations, Composer audit and Docker smoke workflows | Definitions inspected; hosted run results not checked |

Counts above are test files, not test-case counts. Default `artisan test` covers Unit + Feature, not the browser suites. Tests use factories, seed data and database refresh behavior, so isolation is mandatory. Some CI path filters omit display-only Blade/locale changes from Unit/Feature triggers; absence of an automatic CI run is not a pass. Run the planned checks explicitly during implementation.

Known risk from `tests/DuskTestCase.php`: Dusk config overrides persist through `storage/app/duskapiconf_tmp.txt` if a process is killed before cleanup. Diagnose stale overrides in the disposable environment if observed; do not confuse them with a branding change or delete arbitrary user files.

## 10. Day 01 conclusions and boundaries

The audited local branch is an intact YAFFA starting point. A controlled display rebrand is feasible without namespace, API, package, schema or financial changes. README attribution and the local upstream reference are now explicit. Runtime branding remains YAFFA.

The baseline install/run/test gate is blocked, not passed or failed by an application test. No financial logic review, live schema audit, vulnerability assessment, final artifact license clearance or production readiness claim has been completed. The next step is the isolated environment baseline in [CHANGE_PLAN.md](CHANGE_PLAN.md).

## Appendix — Complete baseline text-reference index

This index is generated from the pinned `git grep -I -i -c` query above. Counts are matching lines per file. Technical/historical matches remain intentionally preserved; consult the compatibility register before changing any path. `LICENSE` and the binary asset paths are separately reviewed above and do not need to match this search pattern to be protected.

| Tracked path at baseline | Matching lines |
| --- | ---: |
| `.ai/docs/assets/account-group/overview.md` | 6 |
| `.ai/docs/assets/account/overview.md` | 4 |
| `.ai/docs/assets/budget/budget.md` | 1 |
| `.ai/docs/assets/category/overview.md` | 4 |
| `.ai/docs/assets/currency-rate/overview.md` | 12 |
| `.ai/docs/assets/currency/overview.md` | 12 |
| `.ai/docs/assets/investment-group/overview.md` | 3 |
| `.ai/docs/assets/investment-price/overview.md` | 10 |
| `.ai/docs/assets/investment/overview.md` | 5 |
| `.ai/docs/assets/payee/overview.md` | 1 |
| `.ai/docs/assets/tag/overview.md` | 5 |
| `.ai/docs/assets/transactions/investment-transactions.md` | 2 |
| `.ai/docs/assets/transactions/overview.md` | 2 |
| `.ai/docs/assets/transactions/schedules.md` | 3 |
| `.ai/docs/assets/transactions/standard-transactions.md` | 3 |
| `.ai/docs/assets/transactions/transaction-items.md` | 7 |
| `.ai/docs/assets/transactions/transaction-types.md` | 2 |
| `.ai/docs/features/ai-document-processing/TECHNICAL.md` | 9 |
| `.ai/docs/features/ai-document-processing/ocr/README.md` | 1 |
| `.ai/docs/features/ai-document-processing/overview.md` | 4 |
| `.ai/docs/features/ai-document-retention/architecture.md` | 1 |
| `.ai/docs/features/ai-document-retention/cron.md` | 1 |
| `.ai/docs/features/ai-document-retention/flows.md` | 1 |
| `.ai/docs/features/ai-document-retention/variables.md` | 1 |
| `.ai/docs/features/api-access-and-2fa/SPECIFICATION.md` | 7 |
| `.ai/docs/features/api-access-and-2fa/api-versioning.md` | 1 |
| `.ai/docs/features/api-access-and-2fa/architecture.md` | 2 |
| `.ai/docs/features/api-access-and-2fa/flows.md` | 3 |
| `.ai/docs/features/api-access-and-2fa/permissions.md` | 1 |
| `.ai/docs/features/api-access-and-2fa/tests.md` | 1 |
| `.ai/docs/features/api-access-and-2fa/variables.md` | 6 |
| `.ai/docs/features/budget-schedule-redesign/architecture.md` | 1 |
| `.ai/docs/features/budget-schedule-redesign/variables.md` | 1 |
| `.ai/docs/features/dashboard/onboarding-and-setup.md` | 1 |
| `.ai/docs/features/dashboard/overview.md` | 3 |
| `.ai/docs/features/mobile-app-support/architecture.md` | 3 |
| `.ai/docs/features/precision-improvements/architecture.md` | 1 |
| `.ai/docs/features/qif-csv-import/SPECIFICATION.md` | 3 |
| `.ai/docs/features/qif-csv-import/architecture.md` | 3 |
| `.ai/docs/features/qif-csv-import/flows.md` | 1 |
| `.ai/docs/features/qif-csv-import/tests.md` | 1 |
| `.ai/docs/features/qif-csv-import/variables.md` | 4 |
| `.ai/docs/features/reports/budget-and-schedules.md` | 2 |
| `.ai/docs/features/reports/cash-flow-and-forecasting.md` | 1 |
| `.ai/docs/features/reports/category-based-history-and-forecast-review.md` | 2 |
| `.ai/docs/features/reports/find-transactions.md` | 3 |
| `.ai/docs/features/reports/investment-timeline.md` | 1 |
| `.ai/docs/features/reports/overview.md` | 4 |
| `.ai/docs/product-context.md` | 2 |
| `.ai/docs/specifications/browser-based-locale/specification.md` | 11 |
| `.ai/docs/specifications/budget-schedule-redesign/background.md` | 3 |
| `.ai/docs/specifications/budget-schedule-redesign/forecast-performance.md` | 1 |
| `.ai/docs/specifications/budget-schedule-redesign/recurrence-rrule-storage.md` | 1 |
| `.ai/docs/specifications/budget-schedule-redesign/specification.md` | 6 |
| `.ai/docs/specifications/fast-transaction-entry/concept.md` | 3 |
| `.ai/docs/specifications/investment-account-scope/02-account-investments-card.md` | 1 |
| `.ai/docs/specifications/payee-category-show-pages/specification.md` | 1 |
| `.ai/docs/specifications/precision-improvements/background.md` | 4 |
| `.ai/docs/specifications/precision-improvements/specification.md` | 5 |
| `.ai/docs/specifications/tom-select-migration/specification.md` | 2 |
| `.ai/docs/specifications/tom-select-migration/testing.md` | 1 |
| `.dockerignore` | 1 |
| `.env.ci` | 7 |
| `.env.dusk.ci` | 10 |
| `.env.example` | 15 |
| `.github/copilot-instructions.md` | 2 |
| `.github/workflows/deploy-private.yml` | 2 |
| `.github/workflows/docker-build-contributor.yml` | 2 |
| `.github/workflows/docker-build.yml` | 2 |
| `.github/workflows/docker-smoke-test.yml` | 1 |
| `.github/workflows/test-dusk-critical.yml` | 1 |
| `.github/workflows/test-dusk-extended.yml` | 1 |
| `CHANGELOG.md` | 332 |
| `CLAUDE.md` | 3 |
| `README.md` | 20 |
| `UPGRADE.md` | 43 |
| `app/CLAUDE.md` | 1 |
| `app/Casts/MoneyCast.php` | 5 |
| `app/Console/Commands/DumpDemoDatabase.php` | 1 |
| `app/Console/Commands/PromoteDemoDatabase.php` | 1 |
| `app/Console/Commands/ResetDemoDatabase.php` | 4 |
| `app/Console/Commands/SimulateIncomingEmail.php` | 2 |
| `app/Http/Controllers/API/AiUserSettingsApiController.php` | 1 |
| `app/Http/Controllers/API/ApiTokenApiController.php` | 2 |
| `app/Http/Controllers/API/MetaApiController.php` | 4 |
| `app/Http/Controllers/API/TwoFactorApiController.php` | 4 |
| `app/Http/Controllers/API/UserApiController.php` | 1 |
| `app/Http/Controllers/Auth/RegisterController.php` | 3 |
| `app/Http/Controllers/UserController.php` | 2 |
| `app/Http/Requests/AccountEntityRequest.php` | 1 |
| `app/Http/Requests/ApiTokenRequest.php` | 1 |
| `app/Http/Requests/ImportParseRequest.php` | 1 |
| `app/Http/Requests/SuggestFileImportProfileRequest.php` | 1 |
| `app/Http/Requests/UserRequest.php` | 1 |
| `app/Http/View/Composers/JavaScriptVariablesComposer.php` | 4 |
| `app/Listeners/DataLayerEventForLoginFailed.php` | 2 |
| `app/Listeners/DataLayerEventForLoginSuccess.php` | 2 |
| `app/Listeners/SendLoginFailedNotification.php` | 2 |
| `app/Listeners/SendLoginSuccessNotification.php` | 2 |
| `app/Models/Currency.php` | 1 |
| `app/Notifications/LoginFailedNotification.php` | 1 |
| `app/Notifications/LoginSuccessNotification.php` | 1 |
| `app/Providers/AppServiceProvider.php` | 6 |
| `app/Providers/TelescopeServiceProvider.php` | 1 |
| `app/Services/ApiTokenService.php` | 2 |
| `app/Services/GoogleDriveService.php` | 5 |
| `app/Services/Import/CsvParserService.php` | 1 |
| `app/Services/Import/QifParserService.php` | 2 |
| `composer.json` | 4 |
| `composer.lock` | 13 |
| `config/app.php` | 1 |
| `config/yaffa.php` | 1 |
| `database/factories/GoogleDriveConfigFactory.php` | 1 |
| `database/seeders/DatabaseSeeder.php` | 2 |
| `database/seeders/Fixed/UserSeeder.php` | 1 |
| `deploy.php` | 3 |
| `docker-compose.yml` | 1 |
| `docker-smoke-test.sh` | 1 |
| `docker/docker-compose.yml` | 26 |
| `lang/en.json` | 20 |
| `lang/fr.json` | 20 |
| `lang/hu.json` | 21 |
| `lang/pl.json` | 20 |
| `package-lock.json` | 3 |
| `package.json` | 1 |
| `resources/js/CLAUDE.md` | 1 |
| `resources/js/account/history.js` | 7 |
| `resources/js/account/index.js` | 2 |
| `resources/js/account/show.js` | 10 |
| `resources/js/ai-documents/components/AiDocumentProcessingHistory.vue` | 1 |
| `resources/js/ai-documents/components/AiDocumentTable.vue` | 3 |
| `resources/js/ai-documents/components/AiDocumentViewer.vue` | 1 |
| `resources/js/app.js` | 2 |
| `resources/js/categories/components/CategoryBudgetsCard.vue` | 1 |
| `resources/js/categories/components/CategoryOverviewCard.vue` | 1 |
| `resources/js/categories/components/CategorySchedulesCard.vue` | 1 |
| `resources/js/categories/components/CategoryShowPage.vue` | 1 |
| `resources/js/categories/index.js` | 2 |
| `resources/js/currencies/index.js` | 7 |
| `resources/js/currency-rates/components/CurrencyRateChart.vue` | 2 |
| `resources/js/currency-rates/components/CurrencyRateOverview.vue` | 1 |
| `resources/js/dashboard/components/Dashboard.vue` | 3 |
| `resources/js/dashboard/components/widgets/AccountBalance.vue` | 2 |
| `resources/js/dashboard/components/widgets/AiDocumentSummary.vue` | 1 |
| `resources/js/dashboard/components/widgets/CategoryWaterfall.vue` | 3 |
| `resources/js/dashboard/components/widgets/ScheduleCalendar.vue` | 2 |
| `resources/js/import/components/CsvPreviewTable.vue` | 1 |
| `resources/js/import/components/DuplicateCandidatesPanel.vue` | 1 |
| `resources/js/import/components/ImportDraftTable.vue` | 1 |
| `resources/js/import/components/RelatedAiDocumentsPanel.vue` | 1 |
| `resources/js/import/components/ScheduleCandidatesPanel.vue` | 1 |
| `resources/js/investment-price/components/InvestmentPriceOverview.vue` | 1 |
| `resources/js/investment-price/components/InvestmentPriceOverviewCard.vue` | 1 |
| `resources/js/investments/components/display/AccountDistributionCard.vue` | 1 |
| `resources/js/investments/components/display/InvestmentDetailsCard.vue` | 1 |
| `resources/js/investments/components/display/PriceHistoryCard.vue` | 2 |
| `resources/js/investments/components/display/QuantityHistoryCard.vue` | 2 |
| `resources/js/investments/components/display/ResultsCard.vue` | 2 |
| `resources/js/investments/components/display/TransactionHistoryCard.vue` | 1 |
| `resources/js/investments/index.js` | 3 |
| `resources/js/payee/components/AutoRecordCandidates.vue` | 1 |
| `resources/js/payee/components/PayeeOverviewCard.vue` | 1 |
| `resources/js/payee/components/PayeeProfileCard.vue` | 1 |
| `resources/js/payee/components/PayeeSchedulesCard.vue` | 1 |
| `resources/js/payee/components/PayeeShowPage.vue` | 1 |
| `resources/js/payee/index.js` | 3 |
| `resources/js/reports/budgetchart.js` | 6 |
| `resources/js/reports/cashflow.js` | 7 |
| `resources/js/reports/components/BudgetForm.vue` | 2 |
| `resources/js/reports/components/BudgetQuickView.vue` | 2 |
| `resources/js/reports/components/find-transactions/FindTransactions.vue` | 5 |
| `resources/js/reports/components/find-transactions/TransactionTypeFilterCard.vue` | 2 |
| `resources/js/reports/components/find-transactions/helpers.js` | 2 |
| `resources/js/reports/investment-timeline.js` | 7 |
| `resources/js/reports/schedules.js` | 3 |
| `resources/js/sandbox-components/login-helper.js` | 1 |
| `resources/js/shared/lib/datatable/index.js` | 6 |
| `resources/js/shared/lib/helpers/index.js` | 4 |
| `resources/js/shared/lib/i18n/amcharts.js` | 2 |
| `resources/js/shared/lib/i18n/datatables.js` | 4 |
| `resources/js/shared/lib/i18n/format.js` | 2 |
| `resources/js/shared/lib/i18n/translate.js` | 2 |
| `resources/js/shared/lib/ui/amchartsColorTheme.js` | 1 |
| `resources/js/shared/lib/ui/colorMode.js` | 2 |
| `resources/js/shared/lib/ui/sidebarVisibilityPersistence.js` | 8 |
| `resources/js/shared/ui/RecordOverviewCard.vue` | 1 |
| `resources/js/shared/ui/datatable/EditableDatedValueTable.vue` | 2 |
| `resources/js/shared/ui/datatable/TransactionTable.vue` | 1 |
| `resources/js/shared/ui/date/DateRangeFilterCard.vue` | 1 |
| `resources/js/shared/ui/form/MathInput.vue` | 1 |
| `resources/js/shared/ui/reports/DepositsByParentCategory.vue` | 3 |
| `resources/js/shared/ui/reports/MonthlyBreakdown.vue` | 4 |
| `resources/js/shared/ui/reports/MonthlyTimelineChart.vue` | 3 |
| `resources/js/shared/ui/reports/TransactionSummary.vue` | 4 |
| `resources/js/shared/ui/reports/TransactionWaterfall.vue` | 3 |
| `resources/js/shared/ui/reports/WithdrawalsByParentCategory.vue` | 3 |
| `resources/js/transaction-templates/index.js` | 1 |
| `resources/js/transactions/components/display/Item.vue` | 1 |
| `resources/js/transactions/components/display/Schedule.vue` | 2 |
| `resources/js/transactions/components/display/ShowInvestment.vue` | 2 |
| `resources/js/transactions/components/display/ShowStandard.vue` | 1 |
| `resources/js/transactions/components/form/TransactionFormInvestment.vue` | 2 |
| `resources/js/transactions/components/form/TransactionFormStandard.vue` | 2 |
| `resources/js/transactions/components/form/TransactionItemContainer.vue` | 1 |
| `resources/js/user/AiBehaviorSettings.vue` | 1 |
| `resources/js/user/AiProviderSettings.vue` | 1 |
| `resources/js/user/ApiTokenManager.vue` | 4 |
| `resources/js/user/ChangePassword.vue` | 1 |
| `resources/js/user/GoogleDriveSettings.vue` | 2 |
| `resources/js/user/InvestmentProviderSettings.vue` | 1 |
| `resources/js/user/TwoFactorSettings.vue` | 1 |
| `resources/js/user/UserSettings.vue` | 20 |
| `resources/sass/_custom.scss` | 1 |
| `resources/views/accounts/form.blade.php` | 1 |
| `resources/views/auth/login.blade.php` | 5 |
| `resources/views/auth/register.blade.php` | 4 |
| `resources/views/auth/two-factor-challenge.blade.php` | 3 |
| `resources/views/pages/dashboard.blade.php` | 1 |
| `resources/views/pages/sandbox-terms.blade.php` | 3 |
| `resources/views/template/layouts/page.blade.php` | 10 |
| `resources/views/template/master.blade.php` | 4 |
| `resources/views/template/sandbox-components/body-close.blade.php` | 1 |
| `resources/views/template/sandbox-components/head.blade.php` | 2 |
| `routes/console.php` | 3 |
| `tests/Browser/Pages/Auth/AiProviderSettingsTest.php` | 1 |
| `tests/Browser/Pages/Auth/GoogleDriveSettingsTest.php` | 1 |
| `tests/Browser/Pages/Partials/DataLayerTest.php` | 18 |
| `tests/CLAUDE.md` | 3 |
| `tests/DuskTestCase.php` | 2 |
| `tests/Feature/API/ApiTokenApiControllerTest.php` | 1 |
| `tests/Feature/API/TwoFactorApiControllerAccessTest.php` | 1 |
| `tests/Feature/API/TwoFactorDisableTest.php` | 1 |
| `tests/Feature/API/TwoFactorEnrollmentTest.php` | 1 |
| `tests/Feature/API/V1/AiUserSettingsApiV1Test.php` | 4 |
| `tests/Feature/API/V1/DevicePairingApiV1Test.php` | 8 |
| `tests/Feature/API/V1/ImportApiParseTest.php` | 1 |
| `tests/Feature/API/V1/MetaApiV1Test.php` | 6 |
| `tests/Feature/Auth/ChangePasswordTest.php` | 1 |
| `tests/Feature/Auth/EmailVerificationTest.php` | 2 |
| `tests/Feature/Auth/RegisterTest.php` | 7 |
| `tests/Feature/Console/AiDocumentCleanupScheduleTest.php` | 1 |
| `tests/Feature/CurrencyRateTest.php` | 1 |
| `tests/Feature/GoogleDriveConfigApiControllerTest.php` | 2 |
| `tests/Feature/IncomingEmailTest.php` | 6 |
| `tests/Feature/SandboxTest.php` | 2 |
| `tests/Feature/Services/ApiTokenServiceTest.php` | 2 |
| `tests/Feature/ViewApiDocsGateTest.php` | 6 |
| `tests/PEST/DashboardSmokeTest.php` | 1 |
| `tests/PEST/InvestmentSummaryBrowserTest.php` | 1 |
| `tests/PEST/Pages/AiDocuments/ConfirmAutoRecordedTest.php` | 1 |
| `tests/PEST/Pages/AiDocuments/ManualEntryClosesDocumentTest.php` | 1 |
| `tests/PEST/Pages/Categories/CategoryMergeTest.php` | 1 |
| `tests/PEST/Pages/Categories/CategoryShowPageTest.php` | 1 |
| `tests/PEST/Pages/CategoryLearning/CategoryLearningTest.php` | 1 |
| `tests/PEST/Pages/Investments/InvestmentTransactionHistoryTest.php` | 1 |
| `tests/PEST/Pages/Payees/PayeeDeepLinkTest.php` | 1 |
| `tests/PEST/Pages/Payees/PayeeListSearchTest.php` | 1 |
| `tests/PEST/Pages/Payees/PayeeListTest.php` | 1 |
| `tests/PEST/Pages/Payees/PayeeMergeTest.php` | 1 |
| `tests/PEST/Pages/Payees/PayeeShowPageTest.php` | 1 |
| `tests/PEST/Pages/Payees/PayeeSimilarPayeeTest.php` | 1 |
| `tests/PEST/Pages/Reports/BudgetModalTest.php` | 1 |
| `tests/PEST/Pages/Reports/FindTransactions/FindTransactionsFilterBehaviorTest.php` | 1 |
| `tests/PEST/Pages/Reports/FindTransactions/FindTransactionsReportTabsTest.php` | 1 |
| `tests/PEST/Pages/Reports/ReportAccountFilterTest.php` | 1 |
| `tests/PEST/Pages/TransactionTemplates/TransactionTemplateTest.php` | 1 |
| `tests/PEST/Pages/Transactions/TransactionFormInvestmentModalTest.php` | 1 |
| `tests/PEST/Pages/Transactions/TransactionFormInvestmentStandaloneTest.php` | 1 |
| `tests/PEST/Pages/Transactions/TransactionFormStandardModalTest.php` | 1 |
| `tests/PEST/Pages/Transactions/TransactionFormStandardStandaloneTest.php` | 1 |
| `tests/Unit/Http/View/Composers/JavaScriptVariablesComposerTest.php` | 9 |
| `tests/Unit/Models/CurrencyTest.php` | 2 |
| `tests/Unit/Services/GoogleDriveServiceTest.php` | 5 |
| `tests/Unit/Services/Import/QifParserServiceTest.php` | 1 |
