EQ_RUNNER_REPO_URL = https://github.com/ONSdigital/eq-survey-runner.git
RM_TOOLS_REPO_URL = https://github.com/ONSdigital/rm-tools.git

.PHONY: test unit_tests integration_tests

build: test docker-build

docker-build:
	docker build -t europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/rh-ui .

install:
	pipenv install --dev

lint:
	pipenv run flake8
	pipenv run vulture .

serve:
	pipenv run inv server

run:
	pipenv run inv run

test: install unit_tests

local_test:  start_services wait_for_services setup integration_tests stop_services

live_test: start_services wait_for_services setup live_integration_tests stop_services

wait_for_services:
	pipenv run inv wait

setup:
	./scripts/setup_data.sh ${RM_TOOLS_REPO_URL}

integration_tests:
	pipenv run inv integration

live_integration_tests:
	pipenv run inv integration --live

unit_tests: check flake8 load_templates
	pipenv run inv unittests

coverage:
	pipenv run inv coverage

flake8:
	pipenv run flake8

demo:
	./scripts/start_eq.sh ${EQ_RUNNER_REPO_URL}
	pipenv run inv demo

up:
	./docker/rh-ui-up.sh

down:
	./docker/rh-ui-stop.sh

check:
	pipenv check

load_templates:
	./scripts/load_templates.sh