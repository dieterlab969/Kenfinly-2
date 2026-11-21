# KENFINLY 2.0 — Jenkins deployment

Updated 2026-11-21 (Asia/Saigon). Integration branch: **develop**. Public deployment branch: **deploy/my-kenfinly only**.

Repository: [dieterlab969/Kenfinly-2](https://github.com/dieterlab969/Kenfinly-2). Jenkins job: [kenfinly-2-public-develop](https://build.getkenka.com/job/kenfinly-2-public-develop/). Its historical name preserves build history; the SCM configuration determines the branch.

## Current observed state

- Jenkins is active/enabled. The same job uses Pipeline script from SCM, the deployment branch and GitHubPushTrigger, without periodic develop polling.
- Existing GitHub hook 714280894 is active, push-only, application/json, SSL verification enabled and configured with the matching protected HMAC.
- Real GitHub ping UUID 055d1804-e48b-11f1-815d-f4f68a837e75 returned 200 / `{"status":"ping"}` at **2026-11-21 02:45:31 UTC / 09:45:31 Asia/Saigon**, matching the gateway journal. Post-repair missing/wrong-signature probes still return403.
- The initial wrong-path/form configuration and signature rejection were diagnosed without changing the working network. Only the existing GitHub hook was corrected; no host, source, DB or branch-policy change was needed for that repair.
- **Positive automatic deployment remains pending an approved real deployment-branch event.** A gateway ping intentionally stops before Jenkins. Prior builds #1–#3 were manual; last observed serving application SHA was b76d9c6b082bb8de83ab0da29fd58db5af5c2e68. Do not describe a successful ping or manual build as a verified automatic release.

## Source and trigger contract

| Setting | Required value |
| --- | --- |
| Repository | git@github.com:dieterlab969/Kenfinly-2.git |
| Branch specifier | */deploy/my-kenfinly |
| Refspec | +refs/heads/deploy/my-kenfinly:refs/remotes/origin/deploy/my-kenfinly |
| Definition | Pipeline script from SCM / Jenkinsfile; lightweight checkout false, honor refspec, no tags |
| Trigger | GitHub hook trigger for GITScm polling / githubPush(); no periodic SCM poll |
| Hook URL | https://build.getkenka.com/github-webhook/ |
| Hook format/security | application/json, push only, Active, SSL verification enabled, matching SHA256 HMAC secret |
| Workspace | /var/lib/jenkins/workspace/kenfinly-2-public-deploy-my-kenfinly |

GitHub selects push events at repository level. The gateway filters exact `refs/heads/deploy/my-kenfinly`; signed develop/other refs, PR events and branch deletions must not deploy. Develop remains integration. Use a reviewed promotion into the deployment branch; do not change branch policy to make a test pass.

The single-branch Pipeline does not assume BRANCH_NAME. It uses checkout(scm), verifies GIT_BRANCH, repository/refspec, HEAD and the fetched deployment head, then records one full selected SHA and builds/packages that checkout without fetching again. Final publication/smoke requires the active SHA to match the selected SHA. Native GitHub polling may coalesce rapid updates; this is not a guarantee that every event's after SHA receives a separate deployment.

## Signed route and credential locations

```text
GitHub HTTPS → existing VPS Nginx protected /github-webhook prefix
  → VPS loopback 127.0.0.1:19093 authentication gateway
  → existing WireGuard 10.0.0.1 → 10.0.0.2:8080/github-webhook/
  → Jenkins GitHub plugin → the dedicated single-branch Pipeline
```

The existing Jenkins UI/TLS proxy is retained. The gateway validates this repository's raw-body X-Hub-Signature-256 with constant-time comparison, rejects missing/wrong signatures and enforces JSON. It acknowledges signed ping itself, ignores non-deployment events/refs and forwards valid deployment pushes. Valid other-repository deliveries retain their existing native integration policy. Jenkins global hook-secret settings are shared and must not be changed casually.

| Credential ID / protected location | Purpose |
| --- | --- |
| github-jenkins-key | Existing SSH checkout key; preserve host-key verification |
| kenfinly2-ci-env | Secret file for isolated Linux CI DB and synthetic mail/queue/cache settings |
| kenfinly2-github-webhook-hmac | System-scoped Jenkins Secret Text; never bind to application builds |
| VPS /etc/kenfinly-webhook/github-hmac | Matching root-only HMAC, loaded through systemd credentials |
| Ubuntu /var/www/kenfinly-2-deploy/shared/.env | Persistent application configuration/key, outside Git |

Gateway service: kenfinly-github-webhook.service; source: /usr/local/lib/kenfinly/github_webhook.py. Existing VPS vhost: /etc/nginx/sites-available/build.getkenka.com.conf. No secret belongs in a URL, source file, command output, screenshot, archive or console log. Document identifiers and locations only.

Version-controlled templates remain in docker/deploy/: github_webhook.py, kenfinly-github-webhook.service, nginx-jenkins-webhook.conf, jenkins-job.xml and the inactive secret-free hook template. The job XML intentionally installs disabled by default; activation is an operator decision, not a template edit that silently enables deployments.

## Required checks and deployment safeguards

Jenkins serializes deployments, uses a 35-minute timeout and bounded Linux build resources/CPU/IO priority, installs unchanged dependency locks, checks platform requirements, runs existing JS tests, builds assets before PHP view tests, runs the default PHP suite and packages production-only Linux dependencies. Mac vendor/node_modules/native artifacts are not deployment artifacts.

The reviewed Ubuntu entry points /usr/local/lib/kenfinly/build.sh and release.py are root-owned; source checkout cannot replace these privileged scripts. Artifact publication validates branch/platform/locks and the selected SHA. selected-revision.txt, BUILD_REF, KENFINLY_BUILD.json, deployed-release.json and build descriptions retain identities. A failed check, publication, health response or active-SHA mismatch must fail the build.

The publisher preserves shared .env, APP_KEY, uploaded files and DB. APPLY_REVIEWED_MIGRATIONS defaults false; applying a necessary migration also requires operator-maintained reviewed hashes and an owned backup. Never use migrate:fresh, regenerate the application key, rewind the DB or restore an old DB over live data as part of deployment/rollback. Caches are rebuilt, project workers restarted gracefully and public HTTPS health checked.

## Hosted Actions CI

.github/workflows/kenfinly-ci.yml checks pushes/PRs for develop and deploy/my-kenfinly, plus manual dispatch. Read-only permissions, pinned Actions, PHP 8.4, Composer 2.10.0, Node 24.22.3 and disposable MySQL 8.0.46 keep hosted tests separate from deployment credentials/data. The locked public GitHub npm dependency uses command-scoped HTTPS rewriting; locks are unchanged.

[Develop CI #9](https://github.com/dieterlab969/Kenfinly-2/actions/runs/44661194469) and [deployment-branch CI #6](https://github.com/dieterlab969/Kenfinly-2/actions/runs/44659085896) passed real installs/tests/assets/lock checks. Earlier Composer failures and the intermittent synthetic-email collision are retained as failures in operator evidence, rather than hidden by disabling tests. The three inherited publishing workflows are restricted to kantorge/yaffa; Jenkins is the Kenfinly deployment path.

## Verification and manual fallback

For the next approved real deployment-branch update, capture actual GitHub push delivery ID/ref/after, gateway forward result, Jenkins GitHubPushCause/build number, selected full SHA, successful checks/build/publication, matching active SHA and public /up plus /login health. Confirm no unexpected migration, env/key/storage loss or unrelated pipeline/site change. A redelivery alone does not prove that a new merged commit deployed.

Deploy-capable redelivery or a release-branch push is a production action requiring approval. Ping is safe but intentionally does not exercise Jenkins. Do not create a dummy PR, change application logic or bypass signature/TLS checks to manufacture success.

Manual fallback is authenticated Build with Parameters, ACTION=deploy, migrations false unless separately reviewed. It uses the same deployment-only SCM and safeguards; label it manual. Compatible code rollback uses ACTION=rollback or the operator's release.py rollback after inspecting status. It requires a health-verified prior release and matching schema fingerprint, preserves current data and never restores an old database.

## Troubleshooting and recovery

| Symptom | Check / safe response |
| --- | --- |
| Historical failed-to-connect message | Inspect the actual delivery/time and current DNS/TLS/edge logs before blaming the tunnel |
| Public GET 403 / native GET 405 | Expected method/access rejection; test a valid authenticated POST instead |
| Gateway 400 | Inspect safe error class, length/content/payload and delivery ID; do not assume Jenkins is down |
| Invalid-signature 403 | Correct the matching hook secret and raw-body integrity; never disable authentication |
| Media-type 415 | Set application/json; form payload is incompatible for this repository |
| Gateway 202 / no build | Check intentionally ignored branch/event, deletion and native no-change polling; do not broaden branch filters |
| Gateway 502 / Jenkins UI 502 | Check owned service/listener and VPS-to-home private path; preserve routes/peers |
| Build or migration guard fails | Retain failure/current release; review the actual scoped cause, not locks/tests/data-reset shortcuts |

Before any configuration correction, preserve the exact target file/settings and ownership/mode, plan rollback and compare inspected hashes. Test full Nginx configuration before a justified graceful reload; change no other server block. If validation fails, restore the exact reviewed target change without clobbering concurrent edits. A gateway rollback must not leave an enabled deployment job behind an unsigned public path. Secret rollback cannot be claimed if the previous stored GitHub value was unknown.

Monitor both actual GitHub deliveries and private Jenkins availability: gateway ping alone is not downstream health. Keep payload/signature/credential content out of logs. Primary references: [GitHub signature validation](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries), [Jenkins GitHub trigger](https://www.jenkins.io/doc/pipeline/steps/params/pipelinetriggers/), [SCM checkout](https://www.jenkins.io/doc/pipeline/steps/workflow-scm-step/).
