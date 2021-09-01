# Running RH UI in Docker

Running the RH UI Service (and it's dependencies) in Docker saves any problems with 
local builds and making sure that you are using the correct Python version.

## Prerequisits

### 1. Docker pull permissions

If Docker pull commands fail with a permissions error run the following and re-attempt:

    gcloud auth configure-docker europe-west2-docker.pkg.dev

### 2. Google credentials

The docker compose file for RH depends on the $DOCKER_GCP_CREDENTIALS environment
variable. This must point to a file containing your Google credentials.

Depending on how you've set this up you may need to refresh your credentials by running 
'gcloud auth application-default login' before attempting to start the services.

Alternatively this environment varible may point at locally downloaded credentials for 
your GCP environment, which has the advantage of a one time setup and no more 'gcloud auth'.
To download them login to GCP and switch to your project. Then it's 'menu -> IAM & Admin -> Service Accounts'.
Finally click on the 'Keys' tab then 'Add key -> create new key (Json)'. Google then creates 
and downloads a credentials file.

If your credentials are not valid you can see that the attempt to do an initial write to 
the Firestore startup collection fails. In this circumstance the /info endpoint also 
seems to produce an empty response.

The command to look at the rh-service logs is 'docker logs rh-service'. 

### 3. GCP project 

The name of your GCP project must be set in an environment variable called $GOOGLE_CLOUD_PROJECT,
eg 'sdc-rh-fredf'

### 4. RH-Service is running

As you would expect rh-service needs to be running for Cucumber tests, etc.
This can be started before or after the ui is started.


## Starting & Stopping RH UI

To start and stop the RH Service and it's dependencies (mock-ai & Redis) you
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

If you want to run with a specific release or development build for mock-case or rh-service
the required versions can be set near the top of the rh-docker-service.sh script.

The ordering for doing this should be:

1. Run rh-ui-stop.sh to stop existing services.

1. Amend the versions required in ./rh-ui-up.sh

1. Run rh-ui-up.sh to bring up the new versions. The 'docker pull' command in the script
will download the images if required.
