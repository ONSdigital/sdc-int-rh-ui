# Running RH UI in Docker

Running the RH UI Service (and it's dependencies) in Docker saves any problems with 
local builds and making sure that you are using the correct Python version.

## Prerequisites

### 1. Docker pull permissions

If Docker pull commands fail with a permissions error run the following and re-attempt:

    gcloud auth configure-docker europe-west2-docker.pkg.dev

### 2. RH-Service is running

As you would expect rh-service needs to be running for Cucumber tests, etc.
This can be started before or after the ui is started.


## Starting & Stopping RH UI

To start and stop the rh-ui and it's dependencies (mock-service & Redis) you
can run scripts within the docker directory.

To bring up the services run the following. Note that the script will pull down
the required docker images if they are not already cached on your machine. 

    cd sdc-int-rh-ui
    ./docker/rh-ui-up.sh
    
To stop the services:

    cd sdc-int-rh-ui
    ./docker/rh-ui-stop.sh


## Confirming execution

After start RH UI you can confirm it looks healthy by checking its logs:

    docker logs rh-ui


## Running with specific releases

If you want to run with a specific release or development build for mock-service or rh-ui
the required versions can be set near the top of the rh-ui-up.sh script.

The ordering for doing this should be:

1. Run rh-ui-stop.sh to stop existing services.

1. Amend the versions required in ./rh-ui-up.sh

1. Run rh-ui-up.sh to bring up the new versions. The 'docker pull' command in the script
will download the images if required.


## Example commands to run everything locally

If not using the RH Cucumber local profile, point at the emulator using environment variables:

    export PUBSUB_EMULATOR_HOST="localhost:9808"
    export PUBSUB_EMULATOR_USE="true"

To run the services and Cucumber tests:

    cd /Users/peterbochel/sdc/source
    
    ./sdc-int-rh-service/docker/rh-service-up.sh 
    ./sdc-int-rh-ui/docker/rh-ui-up.sh 
    docker ps
    
    cd sdc-int-rh-cucumber/
    ./run.sh
    cd ..
    
    ./sdc-int-rh-service/docker/rh-service-stop.sh 
    ./sdc-int-rh-ui/docker/rh-ui-stop.sh 
    docker ps

