#!/bin/sh
set -e

#
# This scripts starts the services needed to run RH-ui locally.
# It is intended to be used by developers who have a local RH-service and want to standup RH-ui for:
#   - either local RH-service development
#   - or, to run the RH Cucumber tests.
#
# Prerequisites:
#   - RabbitMQ is running.
#   - Rabbit queues have been created (see RH-service Readme.doc).
#   - RH-service is running.
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

docker compose -f $SCRIPT_DIR/docker-compose-mock-ai.yml up -d

docker compose -f $SCRIPT_DIR/docker-compose-rh-ui.yml up -d
