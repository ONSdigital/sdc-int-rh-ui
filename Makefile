EQ_RUNNER_REPO_URL = https://github.com/ONSdigital/eq-survey-runner.git
RM_TOOLS_REPO_URL = https://github.com/ONSdigital/rm-tools.git

.PHONY: test unit_tests integration_tests

build: test docker-build

docker-build:
	docker build -t europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/sdc-int-rh-ui .

install:
	pipenv install --dev

lint:
	pipenv run flake8
	pipenv run vulture .

serve: # Unmaintained, may fail
	pipenv run inv server

run:
	pipenv run python run.py

test: install unit_tests

wait_for_services:  # Unmaintained, may fail
	pipenv run inv wait

setup: # Unmaintained, may fail
	./scripts/setup_data.sh ${RM_TOOLS_REPO_URL}

integration_tests: # Unmaintained, may fail
	pipenv run inv integration

live_integration_tests: # Unmaintained, may fail
	pipenv run inv integration --live

unit_tests: check flake8 load_templates
	pipenv run pytest tests/unit --cov app --cov-report term-missing --cov-report xml

coverage: # Unmaintained, may fail
	pipenv run inv coverage

flake8:
	pipenv run flake8

demo: # Unmaintained, may fail
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

translate:
	pipenv run pybabel extract -F babel.cfg -o app/translations/messages.pot . 		# update the .pot files basing on templates
	pipenv run pybabel update -i app/translations/messages.pot -d app/translations	# update .po files basing on .pot
	pipenv run pybabel compile -d app/translations									# compile to .mo basing on .po