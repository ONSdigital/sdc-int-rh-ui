ARG  python_pipenv_build_image=europe-west2-docker.pkg.dev/ons-ci-rm/docker/python-pipenv:3.10.13
FROM ${python_pipenv_build_image} as build

ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /app
COPY Pipfile* /app/

RUN /root/.local/bin/pipenv sync

FROM python:3.10.6-slim@sha256:ddfe4839f1516d0484944e07ea22200ede3d48828ecbf1f68eec1a9a06b79406

RUN groupadd -g 984 respondenthome && \
    useradd -r -u 984 -g respondenthome respondenthome
WORKDIR /app
RUN mkdir -v /app/venv && chown respondenthome:respondenthome /app/venv
COPY --chown=respondenthome:respondenthome --from=build /app/.venv/ /app/venv/
COPY --chown=respondenthome:respondenthome . /app/

EXPOSE 9092

USER respondenthome

ENTRYPOINT ["/app/venv/bin/python"]
CMD ["run.py"]