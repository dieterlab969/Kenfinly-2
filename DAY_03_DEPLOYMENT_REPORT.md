# KENFINLY 2.0 — Daily Engineering Report

Date: 2026-11-18 (Asia/Saigon)\
Day: 03 — public Ubuntu deployment phase\
Objective: Establish the public Ubuntu/WireGuard/VPS deployment and a dedicated develop Jenkins pipeline, with real verification and safe code rollback.\
Status: Blocked

The public deployment and manual Jenkins deploy/rollback work are complete. Full sign-off remains blocked by unverified new-commit triggering/external mail delivery and the previously known opening-summary defect. Those limits are not counted as completed. The earlier Day 03 Mac report is preserved as its own dated archive.

## 1. Completed Work

- Reviewed instructions, actual repository state, deployment files, manifests/locks and existing reports before changes. The owner had committed/published the prior local setup as `b76d9c6b082bb8de83ab0da29fd58db5af5c2e68`; the checkout was clean at this task's start. `.ai/rules` remains absent.
- Recorded exact host/runtime/permission/network/migration/rollback changes in `CHANGE_PLAN.md` before execution. This task explicitly authorized the public deployment; no Git push was inferred from that authorization.
- Verified the actual topology: public VPS `210.245.84.76`, WireGuard `10.0.0.1 → 10.0.0.2`, home Ubuntu Nginx 18082, separate loopback FPM 19084. Reused healthy tunnel peers/routes and preserved default routes.
- Preserved `/var/www/Kenfinly-2` and the separate older application. Created dedicated release/shared/current/previous layout, non-login runtime/deployment/database users and a private project MySQL instance/database/users. Existing shared data/credentials were not reused.
- Installed only required PHP 8.4 extensions with a reviewed same-major patch update to 8.4.27; selected private Linux Node 24.22.3 with official checksum verification. Default PHP 8.2, shared Node 20 and other runtime majors remain unchanged.
- Configured root-protected persistent production env/key, APP_DEBUG=false, exact public URLs, host-only secure public session, existing bounded trusted-proxy setting, file cache/session, owned queue and one scheduler timer. No production key rotation or data reset occurred.
- Configured one target virtual host per server, one exact WireGuard ingress allowance, the existing matching public certificate and renewal hook. Selected-lineage renewal simulation passed; no host-key/TLS bypass or forced production certificate renewal.
- Added a scoped WireGuard-only Postfix path with fixed sender and peer restrictions. Registered a dedicated synthetic user, received actual verification mail in the new private VPS mailbox and accepted its signed HTTPS link with email verification enabled.
- Created dedicated Jenkins job `kenfinly-2-public-develop`, used Jenkins credentials storage, validated the definition and completed manual deploy plus B→A→B code switching. Original unrelated job configuration is unchanged.
- Exercised public login, income/expense, queued processing, session/storage persistence, header spoof rejection and browser cookie isolation. Kept the existing full-summary workaround explicit.
- Created six requested deployment documents. Automation/configuration is recorded in local review commit **`2c1aa18fde13a74484801dd8cb475367a4d86e1a`**; no push was performed. Public application source remains the selected remote develop commit **b76d9c6b…**, not an unpublished local commit.
- Removed only task-created administrative/CI secret copies, closed the named temporary operator SSH session, and verified the public app still responds afterward. Runtime secrets remain in their intended protected server/Jenkins stores; synthetic evidence/data is retained.

## 2. Deliverables

| Path | Actual output |
| --- | --- |
| `docs/UBUNTU_SETUP.md` | Exact runtime, layout, users, private DB/configuration and owned services |
| `docs/NETWORK_AND_DOMAIN.md` | Actual proxy/WireGuard route, domain, TLS renewal, SMTP boundaries and network rollback |
| `docs/JENKINS_DEPLOYMENT.md` | Job, branch/refspec, credential IDs, stages/guards and unverified trigger boundary |
| `docs/DEPLOYMENT_RUNBOOK.md` | Deployment, migration approval, code rollback and failure recovery without database rewind |
| `docs/DEPLOYMENT_VERIFICATION.md` | Executed evidence, release identities, synthetic data and completed/blocked matrix |
| `docs/ENVIRONMENT_MATRIX.md` | Independent Mac, public Ubuntu and isolated CI profiles |
| `Jenkinsfile`, `docker/deploy/` | Pipeline, Linux build/release scripts, Nginx/FPM/MySQL/systemd/sudo/Postfix/renewal configuration |
| `CHANGE_PLAN.md`, `README.md` | Implementation/rollback/outcome register and current documentation links |
| `DAY_03_DEPLOYMENT_REPORT.md`, `DAILY_REPORT.md` | This phase's dated report and identical latest report |
| Private ignored evidence | `storage/app/ubuntu-deployment/`: logs, manifests, screenshots and synthetic verification records; never publish wholesale |

Original MIT file, upstream reference/history, prior dated reports, dependency locks and application financial/schema/test source are preserved. Inherited YAFFA UI branding remains visible; APP_NAME is KENFINLY.

## 3. Verification

| Check | Actual result |
| --- | --- |
| Linux locked install/platform/build | Pass; PHP 8.4.27, Node 24.22.3, MySQL 8.0.46; no lock upgrade or Mac artifact reuse |
| Existing PHP/JS suites | **1,806 PHP tests / 6,427 assertions**, **40 JS tests** passed on Linux; separate CI DB only |
| Jenkins #1 | **SUCCESS**, develop deploy, 314.074s; active SHA b76d9c6b… archived |
| Jenkins #2 | **SUCCESS**, B→A code rollback to e3936669…, 8.139s |
| Jenkins #3 | **SUCCESS**, A→B return to current develop, 7.893s; final release `20261118T040320300266Z-b76d9c6b082b-1` |
| Public HTTPS/redirect/renewal | Health/login 200, normal TLS result 0; Chromium TLS 1.3; HTTP 308; selected renewal dry-run/hook exit 0 |
| Registration/email/login | Verification gate retained, actual VPS-mailbox delivery and signed HTTPS link pass; wrong password rejected and correct login succeeds |
| Financial endpoint flow | User 1, payee 1, wallet 2; opening USD 1,000, income 250 (transaction 1), expense 50 (transaction 2) recorded |
| Queue/report | Five pending jobs observed; worker processes the existing full-summary operation, cash 1,200. Initial cash 200 reproduced D02-F01 |
| Deployment and rollback persistence | Same authenticated session, both transactions, USD 1,200 and shared storage marker survive code switches; no DB restore |
| Proxy identity/CSRF | Correlated requests through both proxies/FPM; real client rate-limit count 1 versus spoofed 0; missing/foreign-origin CSRF request rejected 419 |
| Browser/assets/cookies | 0 failed assets/page exceptions; two transaction comments visible; secure host-only public cookie; 0 cookies selected for alpha |
| Secret paths | `/.env`, `/.git/config` 403; `/composer.json` 404 |
| Scheduler/persistence | One enabled timer, owned services enabled/active, due minute commands DONE; no reboot performed |
| Unrelated services/sites | 47 VPS / 22 home original Nginx files checked; only target VPS file changed. Four other sites return 200, Jenkins expected unauthenticated 403; old job config unchanged |
| Mac independence | Trusted alpha health passes, local services remain running, managed Mac env hash unchanged |
| Source checks | Shell/Python syntax and Jenkins linter pass; credential/staged protected-file checks pass; financial/schema/lock/license source unchanged |

Inspected screenshots: `public-dashboard.png`, `public-wallet.png`, `public-history.png` under private evidence. The built UI also displays the deployed b76d9c6b… reference. Browser verification used the already locked standalone Chromium because the in-app/Computer Use state connection was unavailable; no manual GUI pass is claimed.

Initial failures were retained and corrected: stale package indexes, missing curl extension, new build-order/CI-env mistake, project mysqldump option grouping, native FPM log destination, renewal invocation timeout and a private mail-link parser's trailing Markdown character. No application test was weakened to hide them.

## 4. Issues and Risks

- **Automatic change-triggered build is unverified.** Real scheduled polling reports the already-built develop SHA / “No changes”; all three execution causes are manual. No authorized push/new remote event was manufactured.
- **External mail delivery is unverified.** Private SMTP/local VPS delivery works, but no external test recipient or sender-domain SPF/DKIM alignment has been verified. Verification remains enabled.
- **D02-F01 remains open.** The stored opening 1,000 was missing from initial derived cash 200; explicit existing summary rebuild gives 1,200. Passing suites do not establish that the initialization defect is fixed.
- Existing translation baseline remains 308 errors / 91 warnings. Full UI rebranding, full browser/Dusk/cross-browser/nightly integration coverage and real reboot testing remain unverified.
- Existing broadly bound legacy database/Jenkins/tunnel ports predate this task. They were not changed as an unrelated hardening project; new project DB/FPM remain private.
- The rollback drill changes release/Git identity with identical application/schema/lock content. It proves the mechanism and persistence, not compatibility of a future changed schema/application version.

## 5. Changes Made

Home: dedicated release/shared directories and three non-login service identities; PHP 8.4 package/extension update; private Node installation; separate MySQL 13316 and scoped app/CI DBs; existing schema plus seven reviewed migrations on the new app DB; protected env/key/client files; dedicated FPM/queue/timer units; owned AppArmor paths, Nginx site/start ordering, narrow ingress rule and limited deployment sudo rules.

VPS: only the target Nginx route/TLS configuration, certificate-specific renewal hook, a WireGuard-only SMTP listener/sender map, owned Postfix startup ordering and synthetic mailbox identity. Existing public certificate, peers/routes, mail services and unrelated site files remain preserved.

Jenkins: one new job and CI secret-file credential; existing GitHub SSH credential reused through storage; no global executor/runtime change or unrelated pipeline edit. The job is seeded with the reviewed Jenkinsfile until source publication is authorized.

All task-created application data is synthetic and identified in verification docs. Test account password, signed links/cookies and complete env files are excluded from reports/Git. Capacity/load testing and unrelated scaling work were not performed.

## 6. Decisions Required

- Approve/review publication of local automation commits to remote develop, then verify an actual SCM-change-triggered deployment and optionally switch definition loading to SCM.
- Provide a dedicated external recipient and decide sender-domain DNS alignment or dedicated SMTP if external delivery verification is required now.
- Approve a focused D02-F01 regression/fix scope before real-data financial release sign-off; keep formula/schema constraints explicit.
- Prioritize translations and display branding separately. No further approval is needed to inspect/use the current synthetic public deployment.

## 7. Next-Day Plan

1. After authorized publication, observe one real develop-change trigger through successful build/publication and record its actual cause/SHA.
2. Verify external email delivery with an approved recipient/sender configuration; keep verification enabled.
3. Address D02-F01 through a bounded regression and approved implementation, then repeat the unassisted account-opening/report flow.
4. Complete any required remaining browser/integration/reboot verification during an approved maintenance window. Do not reboot a shared host merely for this report.
5. Continue the same reporting format; address translations/approved branding next. Capacity work waits for its own later task.

## 8. Release Readiness

**Operational deployment and manual CI/CD are verified.** DNS/TLS, real proxy/tunnel path, secure sessions, synthetic auth/financial endpoints, local verification mail, worker/scheduler, Linux checks and code rollback have actual evidence. Public source is b76d9c6b… and the Mac remains independent.

**Full sign-off is blocked.** Actual new-commit triggering, external mail deliverability and the known opening-summary initialization defect remain unresolved. No real-data financial release approval, Git push, database rewind, capacity claim or reboot proof is implied.
