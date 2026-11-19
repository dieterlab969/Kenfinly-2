pipeline {
    agent {
        node {
            label 'built-in'
            customWorkspace '/var/lib/jenkins/workspace/kenfinly-2-public-deploy-my-kenfinly'
        }
    }

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        disableResume()
        timeout(time: 35, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '12', artifactNumToKeepStr: '4'))
    }

    triggers { githubPush() }

    parameters {
        choice(name: 'ACTION', choices: ['deploy', 'rollback'], description: 'Rollback changes code only; never restores a database.')
        booleanParam(name: 'APPLY_REVIEWED_MIGRATIONS', defaultValue: false, description: 'Requires the operator-maintained migration hash approval on Ubuntu.')
    }

    environment {
        PATH = "/opt/kenfinly-tools/bin:/opt/kenfinly-tools/node/bin:/usr/bin:/bin"
        DEPLOY_BRANCH = 'deploy/my-kenfinly'
        APP_ORIGIN = 'https://my.kenfinly.com'
    }

    stages {
        stage('Checkout deployment branch') {
            steps {
                script {
                    if (!(params.ACTION in ['deploy', 'rollback'])) {
                        error('Unsupported deployment action.')
                    }
                    def revision = checkout(scm)
                    if (!(revision.GIT_BRANCH in ['origin/deploy/my-kenfinly', 'deploy/my-kenfinly'])) {
                        error('Only deploy/my-kenfinly may deploy this environment.')
                    }
                    if (!(revision.GIT_COMMIT ==~ /[0-9a-f]{40}/)) {
                        error('SCM did not select an exact commit.')
                    }
                    env.RELEASE_SHA = revision.GIT_COMMIT
                    sh '''#!/bin/bash
set -euo pipefail
test "$(git remote get-url origin)" = 'git@github.com:dieterlab969/Kenfinly-2.git'
test "$(git config --get-all remote.origin.fetch)" = '+refs/heads/deploy/my-kenfinly:refs/remotes/origin/deploy/my-kenfinly'
test "$(git rev-parse HEAD)" = "$RELEASE_SHA"
test "$(git rev-parse refs/remotes/origin/deploy/my-kenfinly)" = "$RELEASE_SHA"
'''
                    writeFile(file: 'selected-revision.txt', text: "branch=${env.DEPLOY_BRANCH}\nsha=${env.RELEASE_SHA}\n")
                    archiveArtifacts(artifacts: 'selected-revision.txt', fingerprint: true)
                    currentBuild.description = "${params.ACTION} ${env.DEPLOY_BRANCH} ${env.RELEASE_SHA.take(12)}"
                }
            }
        }

        stage('Linux checks and locked build') {
            when { expression { params.ACTION == 'deploy' } }
            steps {
                withCredentials([file(credentialsId: 'kenfinly2-ci-env', variable: 'CI_ENV_FILE')]) {
                    sh '''#!/bin/bash
set -euo pipefail
set +x
nice -n 10 ionice -c 2 -n 7 /usr/local/lib/kenfinly/build.sh "$WORKSPACE" "$RELEASE_SHA" "$BUILD_NUMBER"
'''
                }
            }
        }

        stage('Publish reviewed release') {
            when { expression { params.ACTION == 'deploy' } }
            steps {
                sh '''#!/bin/bash
set -euo pipefail
set +x
args=()
if [ "${APPLY_REVIEWED_MIGRATIONS:-false}" = true ]; then args+=(--apply-migrations); fi
sudo -n -u kenfinly-deploy /usr/local/lib/kenfinly/release.py deploy \
  "/var/lib/kenfinly-deploy/incoming/$RELEASE_SHA-$BUILD_NUMBER.tar.gz" \
  "$RELEASE_SHA" "$BUILD_NUMBER" "${args[@]}"
'''
            }
        }

        stage('Code rollback') {
            when { expression { params.ACTION == 'rollback' } }
            steps {
                sh 'sudo -n -u kenfinly-deploy /usr/local/lib/kenfinly/release.py rollback'
            }
        }

        stage('Public HTTPS smoke') {
            steps {
                sh '''#!/bin/bash
set -euo pipefail
curl --fail --silent --show-error --max-time 20 "$APP_ORIGIN/up" --output /dev/null
curl --fail --silent --show-error --max-time 20 "$APP_ORIGIN/login" --output /dev/null
sudo -n -u kenfinly-deploy /usr/local/lib/kenfinly/release.py status > deployed-release.json
if [ "${ACTION:-deploy}" = deploy ]; then
  python3 -c 'import json,os; assert json.load(open("deployed-release.json"))["source_sha"] == os.environ["RELEASE_SHA"], "Active release differs from selected commit"'
fi
'''
                archiveArtifacts(artifacts: 'deployed-release.json', fingerprint: true)
                script {
                    def activeSha = sh(returnStdout: true, script: '''python3 -c 'import json; print(json.load(open("deployed-release.json"))["source_sha"])' ''').trim()
                    currentBuild.description = "${params.ACTION} active ${activeSha.take(12)}"
                }
            }
        }
    }
}
