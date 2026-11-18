# KENFINLY 2.0 — public deployment verification

Date: 2026-11-18 (Asia/Saigon). Public URL: **https://my.kenfinly.com**.

Deployment and synthetic checks are executed evidence. Full release readiness remains limited by the known opening-summary defect, unverified external mailbox delivery and the absence of an actual new-commit trigger event. Proposed work is not counted as completed.

## Release identity and executed Jenkins runs

Final selected source: **develop / `b76d9c6b082bb8de83ab0da29fd58db5af5c2e68`**.

- Active release: `20261118T040320300266Z-b76d9c6b082b-1`.
- Linux artifact SHA-256: `c54c10482996052fe5738d9c3a69beda8562a9337b0236bbdcd97a477daee9b1`.
- Compatible rollback baseline: `e3936669c7906550024f56e61aca80cf0d834da8`, release `20261118T035549878434Z-e3936669c790-0`.
- Both source commits have identical app/bootstrap/config/database/resources and lockfile content; their Git references differ. No financial/schema source change was introduced.

| Run | Actual execution |
| --- | --- |
| Initial Linux baseline build | 1,806 PHP tests / 6,427 assertions, 40 JS tests and asset build passed; production dependencies packaged |
| Jenkins #1 | **SUCCESS**, manual `ACTION=deploy`, exact current develop SHA, Linux build/test/platform checks and public smoke; 314.074s |
| Jenkins #2 | **SUCCESS**, code-only B→A rollback; 8.139s; actual active SHA archived |
| Jenkins #3 | **SUCCESS**, A→B return to selected current develop; 7.893s; session, both transactions, USD 1,200 and storage marker retained |

All builds used the dedicated job. No Git push, webhook registration, production DB restore, schema down-migration, dependency-lock update or host reboot was performed. The live job uses the reviewed seeded Jenkinsfile until its version-controlled source is published; application checkout still uses the real develop branch.

## End-to-end results

| Check | Actual result |
| --- | --- |
| DNS / VPS identity | A resolves to 210.245.84.76, matching VPS; no AAAA observed |
| Public TLS | Normal validating curl returns TLS result 0; Chromium validates TLS 1.3 / matching SAN without exceptions; renewal dry-run and selected-lineage hook pass |
| HTTP redirect | Exact hostname redirects to HTTPS; no application login over HTTP |
| Proxy/tunnel path | Correlated edge/home request IDs prove VPS → WireGuard → home 18082 → loopback FPM 19084 |
| Forwarded-header spoofing | Edge replaces injected forwarding headers; application's login counter increments for the actual client, not the injected address (1 versus 0) |
| Registration / verification | Dedicated synthetic user reaches verification gate; actual email delivered to private VPS mailbox; signed public HTTPS link accepted with verification enabled |
| Login | Wrong password rejected, correct login succeeds; CSRF-negative request returns 419 |
| Wallet / income / expense | User 1, wallet 2, payee 1; USD opening 1,000, income 250 (transaction 1), expense 50 (transaction 2) stored through authenticated HTTPS endpoints |
| Background queue | Five pending jobs observed while owned worker paused; resumed worker completes requested summary; resulting cash **1,200** |
| Known financial baseline | Initial report cash was **200**, omitting the opening 1,000. Existing full-summary endpoint produces **1,200**; D02-F01 remains open. This is not a financial fix or an unassisted initialization pass |
| Deployment/session continuity | Same authenticated session remained usable after Jenkins publication; shared key/session/storage retained |
| Rollback preservation | Synthetic transaction amounts, authenticated session, USD 1,200 and storage marker checked after code switches; no DB restore |
| Persistent storage | `shared/storage/app/public/deployment-storage-check-20261118.txt` serves via HTTPS and survives code rollback |
| Runtime safety | Dedicated DB/FPM bind loopback; exact WireGuard ingress; resolved APP_DEBUG=false; Chromium confirms Secure/HttpOnly/Lax host-only cookie and **0 cookies selected for alpha** |
| Browser assets/UI | Built assets only, 0 failed asset responses / page exceptions; two synthetic transaction comments visible; screenshots inspected |
| Secret-path smoke | `/.env` and `/.git/config` return 403; `/composer.json` returns 404; HTTP login redirects 308 to exact HTTPS hostname |
| Unrelated sites/configuration | 47 VPS / 22 home original Nginx files checked; only intended VPS target changed. Four other public sites return 200; unauthenticated Jenkins returns its expected 403. Existing old job unchanged |
| Mac independence | Local trusted HTTPS health passes, owned services remain running, managed Mac `.env` hash unchanged |
| Scheduler / reboot persistence | Owned units enabled; single timer and due jobs configured/observed. No reboot test was performed |
| Build / tests | Existing PHP and JS suites plus reproducible Linux asset build passed; tests targeted only separate CI DB |

Registration/login and API operations used the real public service, not direct database model writes. Read-only database/cache inspection corroborated selected synthetic facts. Not every financial form or external integration was manually clicked; a full browser/Dusk/production load test is not claimed.

## Synthetic data and evidence locations

Test account: `kenfinly-verify@localhost.localdomain`, display name `KENFINLY deployment verification 2026-11-18`; generated password remains only in private evidence storage. This mailbox has a new non-login VPS account, `/var/mail/kenfinly-verify`. It received only synthetic transport/verification checks for this task.

Financial objects are labeled `DEPLOYMENT TEST` / `SYNTHETIC DEPLOYMENT CHECK`; IDs are listed above. Storage marker contains only synthetic text. Data is retained and identified rather than silently removed. No real financial data, demo password or production secret was copied from the Mac.

Private local evidence: `storage/app/ubuntu-deployment/` (ignored, private directory), including:

- `jenkins-build-{1,2,3}.log`, release manifests and Jenkins API/config/linter records.
- `financial-e2e.json`, `email-verification-result.json`, `proxy-and-login-proof.json` and correlated private edge/home logs.
- `rollback-A-proof.json`, `rollback-B-proof.json`, `storage-proof.json`.
- `browser-proof.json`, inspected `public-dashboard.png`, `public-wallet.png`, `public-history.png`.
- `vps-final-audit.json`, `home-final-audit.json`, `unrelated-sites-final.json`, security/config snapshots and runtime/install/publication failure logs.

This directory also contains confidential session/mail/access artifacts. Do not publish it wholesale or paste raw cookies, complete env files or signed links. Public documentation summarizes sanitized results. Server backups/configuration and logs are described in the runbook.

## Initial failures and corrections

| Observation | Bounded correction / outcome |
| --- | --- |
| Stale PHP package index returned 404 | Refreshed metadata; reviewed and installed only the PHP 8.4 package family/extensions; default PHP and Node preserved |
| Locked install refused ext-curl | Installed matching PHP 8.4 curl module; no platform-check bypass |
| View tests lacked Vite manifest | Corrected new build order and private CI env handling; unchanged suite then passed |
| mysqldump rejected generic client database option | Moved it into `[mysql]`; initial guard stopped before migrations; successful owned backup/apply followed |
| FPM could not open container-style stderr descriptor under systemd | Switched owned FPM/PHP logs to private persistent files; dedicated pool starts and passes health checks |
| Initial renewal command outlived SSH timeout | Selected-lineage retry with no random sleep and server-side logging succeeded |
| Mail parser selected a Markdown URL with trailing `)` | Corrected private verification parser; normal signed link succeeds; no authentication/verification policy change |

## Remaining limits and readiness

- **Automatic change-triggered deployment is unverified.** Polling is configured for develop; all recorded deployments/rollbacks were manually started. No authorized push/new remote event was manufactured. Publish/review the prepared automation source and verify the next real SCM-change trigger.
- **External mail deliverability remains unverified.** Real private SMTP/mailbox delivery and signed-link verification pass; no external test recipient or new SPF/DKIM deployment has been verified. Email verification remains enabled.
- **D02-F01 remains open:** initial derived balances can omit opening balance until the existing full-summary action runs. Translation checker baseline remains 308 errors / 91 warnings from the unchanged Day 02 source.
- Full UI rebranding, full browser/Dusk/cross-browser coverage, optional external integrations, real reboot testing and capacity testing are outside the executed scope. Existing broadly exposed legacy ports were not altered as an unrelated hardening change.
- Mac alpha runtime/configuration, original license/history, both lockfiles, unrelated apps/data and existing Jenkins jobs are preserved. Relevant final checks must be read alongside the private evidence, not inferred from this plan.

Infrastructure is available for continued controlled verification with synthetic data. This record does not approve real-data financial release readiness or claim all automated/external-delivery paths have passed.

## Handover status

| Area | Status | Evidence / remaining blocker |
| --- | --- | --- |
| Application deployment | Completed | Selected develop SHA live, Linux build/tests and public smoke pass |
| DNS | Completed | Existing A correctly targets VPS; unchanged |
| WireGuard | Completed | Healthy existing peer path used; peers/routes preserved |
| VPS Nginx | Completed | Exact-host public TLS proxy installed and validated |
| Ubuntu Nginx | Completed | Dedicated WG endpoint and source/Host restrictions validated |
| HTTPS | Completed | Public curl/Chromium validation, redirect, renewal simulation and hook pass |
| Jenkins job | Completed | Dedicated job; deploy and both rollback runs succeeded |
| Automatic trigger verification | Blocked | Polling works; a real new-commit-triggered build awaits an authorized remote develop change |
| Full end-to-end sign-off | Blocked | Controlled synthetic flow passes; external mailbox delivery and D02-F01 remain unresolved |

The code-switch drill uses different Git SHAs with identical application/schema/lock content. It proves the mechanism and persistence, not backward compatibility for a future application/schema change. No real data, database rewind or key rotation was involved.
