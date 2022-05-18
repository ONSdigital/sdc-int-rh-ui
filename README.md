
# Respondent Home Python Web Application
Respondent Home is part of ONS's Survey Data Collection platform. It allows users to validate their Unique Access Code (UAC) and forwards
them to the [ONS eQ Survey Runner](https://github.com/ONSdigital/eq-survey-runner) upon successful validation. It also enables users to request new/replacement UACs.

This repository contains the Python [AIOHTTP](http://docs.aiohttp.org/en/stable/) application that is the user interface for the Respondent Home product.

## Payload

The fields required to launch an eQ survey are documented in the [ons-schema-definitions](http://ons-schema-definitions.readthedocs.io/en/latest/respondent_management_to_electronic_questionnaire.html#required-fields).


## Installation
Install the required Python packages for running and testing Respondent Home within a virtual environment:

  `make install`

## Running
First, run scripts/load_templates.sh to pull the current/correct version of the ONS Design Patterns.

Then to run this application in development use, run 'run.py'

and access using [http://localhost:9092/en/start/](http://localhost:9092/en/start/) or [http://localhost:9092/cy/start/](http://localhost:9092/cy/start/).

You can also run RH UI and its dependencies in Docker.
See the [Readme](docker/README.md) in the docker directory for details.


## Tests
To run the unit tests for Respondent Home:

  `make test`
  
To run the unit tests and generate a coverage report for Respondent Home:

  `make coverage`

To bring up all the RAS/RM & eQ Runner services and run the integration tests against them and Respondent Home:

  `make local_test`

NB: Waiting for the services to be ready will likely take up to ten minutes.


## Docker
Respondent Home is one part of the RAS/RM docker containers:

  [https://github.com/ONSdigital/ras-rm-docker-dev](https://github.com/ONSdigital/ras-rm-docker-dev)

## Translations
The site uses babel for translations.

Text to translate is marked up in html and py templates and files, then a messages.pot is build via pybabel, which collates all the text to translate into a single file.

To build/re-build the translation messages.pot use:

```
pipenv run pybabel extract -F babel.cfg -o app/translations/messages.pot .
```
    
To create a new language messages file, run the following, changing the 2 character language code at the end to the required language code. Only generate a individual language file once.

Note that this implementation includes an English translation. This is needed due to an issue with implementing pybabel with aiohttp.

```
pipenv run pybabel init -i app/translations/messages.pot -d app/translations -l cy
```

Once created, you can update the existing language messages.po files to include changes in the messages.pot by running the following. This will update ALL language files.

```
pipenv run pybabel update -i app/translations/messages.pot -d app/translations
```
    
To compile updates to the messages.po files into messages.mo (the file actually used by the site) use:

```
pipenv run pybabel compile -d app/translations
```
