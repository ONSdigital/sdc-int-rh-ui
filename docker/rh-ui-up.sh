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

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Starting services ..."
COMPOSE_IGNORE_ORPHANS=True docker compose -f $SCRIPT_DIR/docker-compose-rh-ui.yml up -d
