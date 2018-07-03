import logging

from aiohttp.web import Application
from structlog import wrap_logger


logger = wrap_logger(logging.getLogger(__name__))


async def get_case(case_id: str, app: Application):
    async with app.http_session_pool.get(f"{app['CASE_URL']}/cases/{case_id}", auth=app["CASE_AUTH"]) as resp:
        resp.raise_for_status()
        return await resp.json()


async def post_case_event(case_id: str, category: str, description: str, app: Application):
    async with app.http_session_pool.post(
        f"{app.config['CASE_URL']}/cases/{case_id}/events",
        auth=app["CASE_AUTH"],
        json={'description': description, 'category': category, 'createdBy': 'RESPONDENT_HOME'}
    ) as resp:
        resp.raise_for_status()
        return await resp.json()