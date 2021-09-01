#!/bin/sh

#
# This scripts starts the RH UI and its dependencies in docker.
# It is intended to be used by developers who have a local RH-service and want to standup RH-ui for:
#   - either local RH-service development
#   - or, to run the RH Cucumber tests.
#
# This script is compatible with the sdc-int-rh-service/docker/rh-service-up.sh script.
#

set -e

MOCK_AI_VERSION="europe-west2-docker.pkg.dev/ons-ci-int/int-docker-release/mock-ai:latest"
RH_UI_VERSION="europe-west2-docker.pkg.dev/ons-ci-int/int-docker-release/rh-ui:latest"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


echo "1/4 Checking environment variables"
[ -z "$GOOGLE_CLOUD_PROJECT" ] && echo "Need to set GOOGLE_CLOUD_PROJECT" && exit 1;

echo "2/4 Pulling images ..."
docker pull $MOCK_AI_VERSION
docker pull $RH_UI_VERSION

echo "3/4 Tagging images ..."
docker tag $MOCK_AI_VERSION mock-ai
docker tag $RH_UI_VERSION rh-ui

echo "4/4 Starting services ..."
docker compose -f $SCRIPT_DIR/docker-compose-redis.yml up -d
docker compose -f $SCRIPT_DIR/docker-compose-mock-ai.yml up -d
docker compose -f $SCRIPT_DIR/docker-compose-rh-ui.yml up -d
