FROM europe-west2-docker.pkg.dev/ons-ci-rm/docker/python-pipenv:latest as build

ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /app
COPY Pipfile* /app

RUN /root/.local/bin/pipenv sync

FROM python:3.10.6-alpine@sha256:5b4e425e03038da758a35dc6f4473b4cf9bbadb9a7cdc2766d5d1d10ef1c9ca9

RUN addgroup --gid 984 respondenthome && \
    adduser --system --uid 984 respondenthome respondenthome

WORKDIR /app
RUN mkdir -v /app/venv && chown respondenthome:respondenthome /app/venv
COPY --chown=respondenthome:respondenthome --from=build /app/.venv/ /app/venv/
COPY --chown=respondenthome:respondenthome . /app

EXPOSE 9092

USER respondenthome

ENTRYPOINT ["/app/venv/bin/python"]
CMD ["run.py"]
