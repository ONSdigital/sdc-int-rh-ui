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

MOCK_AI_VERSION="europe-west2-docker.pkg.dev/ons-ci-int/int-docker-release/mock-service:latest"
RH_UI_VERSION="europe-west2-docker.pkg.dev/ons-ci-int/int-docker-release/rh-ui:latest"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


echo "1/3 Pulling images ..."
docker pull $MOCK_AI_VERSION
docker pull $RH_UI_VERSION

echo "2/3 Tagging images ..."
docker tag $MOCK_AI_VERSION mock-service
docker tag $RH_UI_VERSION rh-ui

echo "3/3 Starting services ..."
docker compose -f $SCRIPT_DIR/docker-compose-redis.yml up -d
docker compose -f $SCRIPT_DIR/docker-compose-mock-service.yml up -d
docker compose -f $SCRIPT_DIR/docker-compose-rh-ui.yml up -d
