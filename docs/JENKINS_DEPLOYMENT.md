# KENFINLY 2.0 — Jenkins deployment

Dedicated job: **[kenfinly-2-public-develop](https://build.getkenka.com/job/kenfinly-2-public-develop/)**. Deployment branch: **develop** only.

## Actual installation and configuration

The existing Jenkins 2.555.2 controller and built-in Linux executor run on home Ubuntu, user `jenkins`, with two shared executors. No Jenkins upgrade, global executor change or modification of the unrelated `kenfinly-staging` / `flowcut-deploy-pipeline` jobs was performed. The former deploys a different repository's `staging` branch.

- Source repository: `git@github.com:dieterlab969/Kenfinly-2.git`.
- Branch/refspec: `*/develop`, `+refs/heads/develop:refs/remotes/origin/develop`, no tag fetch.
- GitHub credential: existing Jenkins SSH credential `github-jenkins-key`; host verification uses existing trusted known-hosts configuration.
- CI credential: new secret file `kenfinly2-ci-env`, scoped logically to the disposable `kenfinly2_ci` DB; contains no production application credentials.
- Workspace: `/var/lib/jenkins/workspace/kenfinly-2-public-develop`.
- Operational scripts: root-owned `/usr/local/lib/kenfinly/{build.sh,release.py}`; source counterparts under `docker/deploy/`.
- Definition source: repository-root `Jenkinsfile`, validated with the installed Declarative linter.

**No Git push was authorized or performed.** The live job was bootstrapped with an exact reviewed copy of the local Jenkinsfile. It is not currently loading an unpublished Jenkinsfile from GitHub. Review/publish the prepared files before switching the job to “Pipeline script from SCM”, repository/credential above, branch `*/develop`, script path `Jenkinsfile`. Installing reviewed operational script updates remains a controlled Ubuntu administrator action; application commits cannot overwrite the root-owned deployment entry points.

The in-app/Computer Use state connection was unavailable. Authenticated Jenkins API operations, installed linter results, build causes, console logs and archived release manifests provide the configuration/execution evidence; no successful GUI interaction is claimed.

## Pipeline stages and guards

1. Checkout only develop and record its exact commit SHA.
2. Bind the CI secret file; install locked Composer packages and run platform checks, `npm ci`, JS tests, asset build and existing PHP tests on Linux. Build assets before view-rendering tests. Use a private, temporary CI `.env`; remove only its unchanged owned copy.
3. Install production-only PHP dependencies. Package tracked source at the exact SHA plus Linux vendor/built assets, with `BUILD_REF` and `KENFINLY_BUILD.json`; exclude runtime configuration/storage and node_modules.
4. Run `release.py` as non-root `kenfinly-deploy` through a narrowly scoped sudo rule. Verify artifact/platform/lock identities, preserve shared `.env`/storage, enforce migration review, cache supported application files and atomically switch current.
5. Gracefully reload the dedicated FPM and restart the owned queue with a 300s stop allowance. Run public TLS health/login checks; archive `deployed-release.json` and verify active SHA matches the selected deployment SHA.

Jenkins prevents concurrent runs; a host-side flock also serializes manual and Jenkins publications. Builds have a 35-minute timeout, low CPU/IO priority, Composer download parallelism 2, Node heap limit 1536 MiB and serial PHP tests with a process-only 1 GiB limit. Other jobs/services were not globally throttled or reconfigured.

Parameters:

| Name | Default / effect |
| --- | --- |
| `ACTION` | `deploy`; alternatively `rollback` selects the compatible previous code release |
| `APPLY_REVIEWED_MIGRATIONS` | false; true alone is insufficient without matching root-owned migration approvals |

The release helper never runs as root, runs only exact owned service actions through sudo, never regenerates APP_KEY, and never restores a database. Rollback requires prior successful health verification and the same schema fingerprint, rebuilds caches using current shared configuration, and records the actual active SHA. See [DEPLOYMENT_RUNBOOK.md](DEPLOYMENT_RUNBOOK.md).

## Executed builds and trigger boundary

Build #1 manually deployed current develop `b76d9c6b082bb8de83ab0da29fd58db5af5c2e68`: **SUCCESS**, 1,806 PHP tests / 6,427 assertions, 40 JS tests, locked build and public smoke checks. The previous baseline `e3936669c7906550024f56e61aca80cf0d834da8` was independently built/tested on Linux; its application/lock/migration content is identical to current develop, making the rollback drill safe.

Code rollback and return results are recorded in [DEPLOYMENT_VERIFICATION.md](DEPLOYMENT_VERIFICATION.md), including the actual active SHAs, data/session/storage checks and Jenkins build numbers. Build descriptions and archived manifests identify the active release, rather than confusing the rollback target with the SCM checkout SHA.

Scheduled polling was observed: trusted known-host verification, the already-built develop SHA, and “No changes”. SCM polling is configured every five minutes (`H/5 * * * *`) using the selected develop ref only. No GitHub webhook/token was created and no synthetic “SCM cause” was fabricated. **A deployment caused by an actual new remote commit has not been verified**, because this task did not push repository changes. Scheduled polling/configuration is separate evidence from an actual automatic deployment. Keep automatic-trigger verification pending until the next authorized develop change.

Do not use the inherited upstream-targeting `deploy.php` or release workflows for this environment. They remain unchanged and were not triggered by this work.
