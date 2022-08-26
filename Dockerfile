FROM europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/python-pipenv:latest as build

ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /app
COPY Pipfile* /app

RUN /root/.local/bin/pipenv sync

FROM python:3.10.4-alpine@sha256:54293681b8873556d38a4e6b04f52f4ac5c1d305ecf893a369892550d81b7c48

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
