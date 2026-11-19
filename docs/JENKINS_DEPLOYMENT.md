# KENFINLY 2.0 — Jenkins deployment

Updated 2026-11-19 (Asia/Saigon). **Integration: `develop`. Deployment: `deploy/my-kenfinly` only.**

Repository: [dieterlab969/Kenfinly-2](https://github.com/dieterlab969/Kenfinly-2). Existing dedicated job: [kenfinly-2-public-develop](https://build.getkenka.com/job/kenfinly-2-public-develop/). The historical job name is retained to preserve its history; it does not determine the source branch.

## Actual status and prepared configuration

| Area | Observed state |
| --- | --- |
| Controller | Recovered on 2026-11-19; Jenkins 2.555.2 on home Ubuntu, existing built-in Linux executor |
| Existing Kenfinly job | **Disabled**, no queued/running build, last build #3 SUCCESS. Its historical inline/develop definition is retained while activation is pending |
| Local branch | `deploy/my-kenfinly` created from reviewed `ea29ab3c`; application/schema/lock/license content matches the serving application baseline |
| Remote refs | Remote develop is `b76d9c6b082bb8de83ab0da29fd58db5af5c2e68`; no remote `deploy/my-kenfinly` at inspection |
| New SCM/job definition | Prepared locally in `docker/deploy/jenkins-job.xml`, deliberately disabled; not installed/activated |
| GitHub configuration access | Existing browser can open repository Settings → Webhooks; no hook currently configured for this repository. `gh` CLI is not authenticated |
| Signed receiver / HMAC credential | Gateway, systemd/Nginx configuration and inactive hook payload prepared locally; receiver/credential/hook not installed or created |
| Automatic deployment | **Not verified**. No remote push, dummy PR, webhook redelivery or new deployment build was performed |

No push is authorized. Do not enable the old inline job: it still contains the obsolete develop workflow. Keep the deployment job disabled until the exact new source, operational guards and signed receiver are installed together. The public app remains on its previously verified release; pausing Jenkins does not stop it.

## Source workflow and exact commit

1. Merge ordinary feature PRs into **develop** for integration. These updates must not deploy the public application.
2. Review a promotion PR from develop into **deploy/my-kenfinly**, including any lock/schema changes and the deployment configuration. Retain deployment-only guards when resolving conflicts.
3. After activation, a push updating that deployment branch, including a merged promotion PR, reaches the signed hook gateway and Jenkins' existing GitHub push integration.
4. The single-branch SCM job selects/checks out the deployment revision. The Pipeline records its full SHA once and builds/packages that checkout without fetching again. Publication and final smoke require the active SHA to equal that selected SHA.

GitHub's repository webhook selects **push events**, not branches. Branch filtering is enforced by the receiver, exact SCM configuration and Pipeline/build/artifact guards. PR validation events, develop/other-branch pushes and branch deletion do not deploy this application. Native GitHubPushTrigger performs SCM polling and may coalesce rapid pushes; it does not promise a separate deployment of every webhook payload's `after` SHA. The recorded build-selected SHA is the deployment identity.

The Pipeline does not assume `BRANCH_NAME`, which belongs to multibranch jobs. It uses `checkout(scm)`, verifies returned `GIT_BRANCH`, the exact repository/fetch configuration, `HEAD` and the fetched deployment head. Job configuration must be **Pipeline script from SCM**, not the old inline definition.

## Exact job, runtime and credential configuration

- SCM URL: `git@github.com:dieterlab969/Kenfinly-2.git`.
- Branch specifier: `*/deploy/my-kenfinly`.
- Refspec: `+refs/heads/deploy/my-kenfinly:refs/remotes/origin/deploy/my-kenfinly`.
- Script path: `Jenkinsfile`; lightweight checkout false; honor refspec; no tags; no arbitrary branch/SHA parameter.
- Trigger: `githubPush()` / **GitHub hook trigger for GITScm polling**. The old periodic develop poll is removed in the prepared definition.
- Workspace: `/var/lib/jenkins/workspace/kenfinly-2-public-deploy-my-kenfinly`. A new project workspace preserves the old workspace and prevents a stale develop fetch configuration from being normalized or wiped.
- Existing Ubuntu toolchain: PHP 8.4.27, private Linux Node 24.22.3; use Linux installs/assets, never Mac vendor/native artifacts.
- Root-owned operational scripts: `/usr/local/lib/kenfinly/{build.sh,release.py}` on Ubuntu. Their reviewed branch-aware updates must be installed by an operator; source checkout cannot replace these privileged entry points.

| Credential ID | Purpose / state |
| --- | --- |
| `github-jenkins-key` | Existing SSH checkout credential; existing host-key verification retained |
| `kenfinly2-ci-env` | Existing secret file for the isolated CI DB, array mail and sync queue; no production credentials |
| `kenfinly2-github-webhook-hmac` | **Planned** system-scoped Secret Text for hook authentication; do not bind it to the application build |

Never put a secret in a webhook URL, Jenkinsfile, Git config, command-line password, archived build file or console log. Activation must mirror the same HMAC value securely to root-only VPS `/etc/kenfinly-webhook/github-hmac`; the service loads it through systemd credentials. Generate/store without stdout, use a high-entropy value, and do not replace unrelated credentials. No HMAC value was generated during local preparation.

## Signed public webhook route

Webhook URL: **`https://build.getkenka.com/github-webhook/`**, JSON content type, push event only, SSL verification enabled. `docker/deploy/github-webhook.json` is an inactive, secret-free template; its secret must be populated securely during actual setup.

```text
GitHub HTTPS
  → existing VPS Nginx /github-webhook/ only
  → loopback 127.0.0.1:19093 authentication gateway
  → existing WireGuard 10.0.0.1 → 10.0.0.2:8080/github-webhook/
  → existing GitHub plugin → single-branch Pipeline
```

The normal Jenkins UI proxy and certificate stay in their existing virtual host. No new public port or anonymous administration access is required. Current VPS file: `/etc/nginx/sites-available/build.getkenka.com.conf`; it already forwards the UI through the tunnel. No proxy change was needed for controller recovery.

Two unrelated jobs already use GitHubPushTrigger. A first global hook secret could reject their existing deliveries. Instead the prepared `github_webhook.py` validates **this repository's** raw-body `X-Hub-Signature-256` HMAC using constant-time comparison, rejects missing/wrong signatures, recognizes canonical/URL repository identities, and filters exact `refs/heads/deploy/my-kenfinly`. Signed ping is acknowledged; other events/branches are ignored. Valid other repositories' JSON or legacy form deliveries retain their bytes/signatures and existing upstream policy. The 10 MiB body limit is explicit; oversized deliveries fail rather than bypass validation.

The **existing shared hook endpoint** must pass through this gateway; leaving an alternative public unfiltered path would bypass Kenfinly's signature policy. The gateway runs only on loopback on the VPS, uses no third-party Python package, and forwards to the existing private handler. Do not change Jenkins' global GitHub secret policy or other jobs. If a later global policy change is separately approved, assess its interaction with this repository before activation.

Prepared files:

- `docker/deploy/github_webhook.py`: authentication/filter/forwarding; sanitized delivery-ID/status audit only.
- `docker/deploy/kenfinly-github-webhook.service`: DynamicUser, systemd credential loading, loopback service, resource/filesystem restrictions.
- `docker/deploy/nginx-jenkins-webhook.conf`: exact TLS-vhost location, POST only, raw-body buffering, no new admin route.
- `docker/deploy/jenkins-job.xml`: same job, SCM source and disabled state.

## Deployment safeguards retained

The Pipeline serializes runs, uses a 35-minute timeout and low CPU/IO priority, bounds Composer/Node/PHP build resources, installs exact locks, runs JS tests, builds assets before PHP view tests, runs the existing PHP suite and packages production-only Linux dependencies. No lock update or platform-check bypass is permitted.

`selected-revision.txt`, `BUILD_REF`, `KENFINLY_BUILD.json`, archived `deployed-release.json` and build descriptions record selected/active identity. Build and artifact publication reject other branches/platforms. Final HTTPS health/login or SHA mismatch fails the build. No exception is swallowed to make deployment green.

The non-root publisher keeps shared `.env`, APP_KEY, storage/uploads and database, checks reviewed migration hashes and explicit `APPLY_REVIEWED_MIGRATIONS=false` by default, takes an owned backup before approved migration apply, refreshes caches, restarts project workers gracefully and checks public health. It never runs migrate:fresh, generates a replacement key or restores an old database over live data. Code rollback requires a health-verified compatible prior schema fingerprint. Existing same-schema old releases remain eligible for code rollback even though their historical manifest branch is develop.

Parameters remain `ACTION=deploy|rollback` and `APPLY_REVIEWED_MIGRATIONS`; unsupported actions fail. See [DEPLOYMENT_RUNBOOK.md](DEPLOYMENT_RUNBOOK.md).

## Activation sequence — not executed

1. Review the local branch commit and its application/lock/schema diff. Keep the live job disabled and retain its backup. Publish **only after explicit push authorization**:

   ```bash
   git push -u origin deploy/my-kenfinly
   ```

2. On Ubuntu, back up and install the reviewed branch-aware `build.sh` and `release.py` as root-owned operational scripts. Preserve shared application configuration, key/data and existing rollback releases.
3. Update the **same** Jenkins job with the prepared SCM XML while disabled; inspect the saved branch/refspec/credential, default parameters and GitHub trigger. Validate the published Jenkinsfile with the installed linter. Do not leave an independent enabled old deploy job or old poll.
4. Store the planned HMAC credential securely and its matching root-only VPS copy. Check loopback port 19093 is unused. Install the gateway/unit; verify the unit on the actual host, daemon-reload and enable/start only that new service. Its local `/up` check proves liveness, not signature handling.
5. Back up only the Jenkins VPS vhost; insert the prepared exact hook location, run full `nginx -t`, then gracefully reload only after it passes. Preserve TLS renewal, the UI route, other sites and WireGuard. Check unsigned Kenfinly rejection and signed ping/non-deployment branch handling before allowing deployment.
6. In this repository's GitHub Webhooks settings, create the HTTPS JSON push hook with the securely supplied secret and SSL verification on. Verify an actual GitHub ping/delivery response. Do not mistake a local fixture or hook redelivery for a newly merged-commit deployment.
7. Enable the new SCM job only when all guards and receiver settings are ready. Make one separately authorized real update/promotion to **deploy/my-kenfinly**. Observe the complete chain and record the evidence below. Develop-only updates must remain non-deploying.

If activation must be rolled back, disable this project job first. Restore only the saved vhost location/unit/project scripts or job definition as reviewed, retaining the disabled deployment state. A gateway rollback must not leave an enabled target job reachable through an unsigned path. Never reactivate develop deployment or rewind the database as rollback.

## Executed evidence and remaining sign-off

| Check | Actual evidence |
| --- | --- |
| Last deployed application | `b76d9c6b082bb8de83ab0da29fd58db5af5c2e68`, release `20261118T040320300266Z-b76d9c6b082b-1`; unchanged during recovery |
| Prior Jenkins runs | #1 manual deploy SUCCESS (1,806 PHP tests / 6,427 assertions, 40 JS tests); #2 manual code rollback SUCCESS; #3 manual return SUCCESS. All predate this new workflow |
| New automatic build number / SHA | **None**; no push/merge/new automatic deployment observed |
| Controller recovery | Reset failed start state and started once; active/enabled, Result=success, NRestarts=0, public TLS login 200 and authenticated API usable |
| Existing job safety | Old target job disabled, buildable=false, no queued/running build, last build still #3 |
| Other jobs | `kenfinly-staging` and `flowcut-deploy-pipeline` XML hashes match their pre-recovery values |
| Local checks | 27 synthetic payload/HMAC/artifact/HTTP cases pass, including develop/PR/signature rejection, other-repository forwarding and upstream failure propagation; no real hook/build/DB contacted |
| Configuration checks | Shell/Python/XML checks; installed Jenkins Declarative linter passes; VPS Nginx candidate syntax and corrected systemd unit verification pass |
| Runtime scope | Receiver/secret/SCM replacement remain local preparation; root-owned Linux build/release scripts are not yet updated |

Private evidence under ignored `storage/app/ubuntu-deployment/`: `branch-local-checks.json`, `branch-validation.py`, `branch-vps-config-checks-final.json`, `branch-jenkins-recovered.json`, `branch-home-inspection.json`, `branch-jenkins-failure.json`, `branch-git-baseline.json`. Do not publish private access/session files wholesale.

Real activation evidence must include GitHub delivery ID/event/ref/after/result, receiver audit, Jenkins build number and GitHub push cause, selected checkout SHA, completed checks/publication, active release SHA and normal public TLS health. If native polling coalesces pushes, identify the selected current deployment-head SHA rather than asserting an older event SHA was deployed. Webhook redelivery alone does not prove new source deployment. Full end-to-end automation remains unverified until those observations exist.

## Jenkins stopped-service recovery and troubleshooting

On 2026-11-19 the controller was failed with `start-limit-hit`, no 8080 listener, and public proxy 502. The journal shows successful initialization followed by stop requests; no OOM indication was found in the inspected interval. Disk/memory were available. The actor issuing the previous stops is not established by available logs. Service/Java/Jenkins/plugin versions and start limits were not changed.

Before starting, backed up only this project's config to `/var/backups/kenfinly-2/20261119-branch/jenkins-config.xml` and atomically changed its disabled flag while preserving ownership/mode. No target queue item existed. Then executed:

```bash
sudo systemctl reset-failed jenkins.service
sudo systemctl start jenkins.service
```

Startup completed at **2026-11-19 10:41:14 UTC / 17:41:14 Asia/Saigon**. Existing job history/credentials and unrelated job configuration are preserved. These commands are a bounded recovery, not a restart loop; investigate any recurring stop rather than repeatedly clearing the limit.

| Symptom | Action |
| --- | --- |
| Public Jenkins 502 | Check home service, listener and `curl http://127.0.0.1:8080/login`, then VPS-to-home path. Do not replace WireGuard/default routes |
| Start-limit-hit | Inspect journal/stop callers/resources first; pause obsolete target triggers before bounded recovery. Do not disable systemd's protection globally |
| GitHub 403 | Check the exact repository, JSON content type, matching protected HMAC and unmodified raw bytes/signature headers. Never turn off validation |
| GitHub 202 but no build | Could be an intentionally ignored ref/event. Check actual ref, receiver audit, job disabled state, selected branch availability and SCM polling log |
| Hook endpoint succeeds but no new deployment | Require actual build cause/selected SHA; no-change polling, signed ping and redelivery are not a new-commit deployment |
| Fetch/config guard fails | Inspect saved SCM/refspec/workspace. Preserve unexpected `.env` or source; do not weaken the branch/SHA check |
| Migration/publication/health failure | Keep failed status and inspect the owned logs/approval. Preserve current data and use only compatible code rollback |

Manual fallback after activation: authenticated **Build with Parameters**, `ACTION=deploy`, migration flag false unless separately reviewed; it still checks out only the deployment branch and runs the same checks. While activation is pending, do not enable the old inline job. Emergency compatible code rollback can use the existing operator `release.py rollback` path in the runbook; it never publishes arbitrary new source or restores a database.

Primary references: [Jenkins GitHub trigger](https://www.jenkins.io/doc/pipeline/steps/params/pipelinetriggers/), [Git checkout](https://www.jenkins.io/doc/pipeline/steps/workflow-scm-step/), [multibranch variables](https://www.jenkins.io/doc/book/pipeline/multibranch/), [GitHub webhook signatures](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries).
