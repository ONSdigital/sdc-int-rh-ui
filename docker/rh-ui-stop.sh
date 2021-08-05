#!/bin/sh
set -e

# 
# This script stops the docker containers started by 'rh-ui-up.sh'
# 

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

docker compose -f $SCRIPT_DIR/docker-compose-mock-ai.yml stop

docker compose -f $SCRIPT_DIR/docker-compose-rh-ui.yml stop
