import os
import sys

from envparse import ConfigurationError, Env
from invoke import task, run as run_command

env = Env()


@task
def server(_ctx, port=None, reload=True, debug=False, production=True):
    """Run the gunicorn server"""
    try:
        port = port or env('PORT')
    except ConfigurationError:
        print(
            'Port not set. Use `inv server --port=[INT]` or set the PORT environment variable.'
        )
        sys.exit(1)

    log_level = 'DEBUG' if debug else 'INFO'

    if production:
        os.environ['APP_SETTINGS'] = 'ProductionConfig'

    command = (
        'gunicorn "app.app:create_app()" -w 4 '
        f'--bind 0.0.0.0:{port} --worker-class aiohttp.worker.GunicornWebWorker '
        f'--access-logfile - --log-level {log_level}')

    if reload:
        command += ' --reload'
    run_command(command, echo=True)


@task
def flake8(_ctx):
    """Run flake8 on the codebase"""
    run_command('flake8 app', echo=True)


@task
def unittests(_ctx):
    """Run the unit tests"""
    import pytest

    return pytest.main(['tests/unit'])


@task(pre=[flake8])
def test(ctx, clean=False):
    """Run all the tests."""

    if clean:
        cleanpy(ctx)
    return_code = unittests(ctx) or smoke(ctx) or integration(ctx)
    sys.exit(return_code)


@task
def smoke(_ctx, local=False):
    """Run the smoke tests."""
    import pytest

    if local:
        os.environ['RESPONDENT_HOME_URL'] = 'http://localhost:9092'
        os.environ['RESPONDENT_HOME_INTERNAL_URL'] = 'http://localhost:9092'
    retcode = pytest.main(['tests/smoke'])
    sys.exit(retcode)


@task
def integration(ctx, clean=False, live=False):
    """Run the integration tests."""
    import pytest

    if clean:
        cleanpy(ctx)
    if live:
        os.environ['LIVE_TEST'] = 'true'
    retcode = pytest.main(['tests/integration'])
    sys.exit(retcode)


@task
def cleanpy(_ctx):
    """Clear out __pycache__ directories."""
    run_command("find . -path '*/__pycache__/*' -delete", echo=True)
    print('Cleaned up.')


@task
def demo(_ctx):
    """Run the demo server"""
    run_command('python -m tests.demo')


@task
def wait(_ctx):
    from tests.wait_for_services import check_all_services
    check_all_services()
    print('all services are up')


@task
def coverage(_ctx):
    """Calculate coverage and render to HTML"""
    run_command(
        'pytest tests/unit --cov app --cov-report html --ignore=node_modules')
