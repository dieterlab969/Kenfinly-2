pipeline {
    agent { label 'built-in' }

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        disableResume()
        timeout(time: 35, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '12', artifactNumToKeepStr: '4'))
    }

    triggers { pollSCM('H/5 * * * *') }

    parameters {
        choice(name: 'ACTION', choices: ['deploy', 'rollback'], description: 'Rollback changes code only; never restores a database.')
        booleanParam(name: 'APPLY_REVIEWED_MIGRATIONS', defaultValue: false, description: 'Requires the operator-maintained migration hash approval on Ubuntu.')
    }

    environment {
        PATH = "/opt/kenfinly-tools/bin:/opt/kenfinly-tools/node/bin:/usr/bin:/bin"
        DEPLOY_BRANCH = 'develop'
        APP_ORIGIN = 'https://my.kenfinly.com'
    }

    stages {
        stage('Checkout develop') {
            steps {
                script {
                    def revision = checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/develop']],
                        userRemoteConfigs: [[
                            url: 'git@github.com:dieterlab969/Kenfinly-2.git',
                            credentialsId: 'github-jenkins-key',
                            refspec: '+refs/heads/develop:refs/remotes/origin/develop'
                        ]],
                        extensions: [[$class: 'CloneOption', honorRefspec: true, noTags: true, shallow: false]]
                    ])
                    if (!(revision.GIT_BRANCH in ['origin/develop', 'develop'])) {
                        error('Only develop may deploy this environment.')
                    }
                    env.RELEASE_SHA = revision.GIT_COMMIT
                    currentBuild.description = "${params.ACTION} develop ${env.RELEASE_SHA.take(12)}"
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
