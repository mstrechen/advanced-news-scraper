import logging

from sqlalchemy.exc import SQLAlchemyError

from admin import celery
from admin.models.sites import Site
from admin.app import db, app

from scraping.tasks.parse_news_list import parse_news_list_task

logger = logging.getLogger(__name__)


def fetch_site_parser_ids():
    with app.app_context():
        site_parser_ids = db.session.query(Site.active_parser_id).all()

    return site_parser_ids


@celery.task(queue='test')
def run_site_parsers_task():
    try:
        site_parser_ids = fetch_site_parser_ids()
    except SQLAlchemyError:
        return dict(result='FAILURE', comment="Fetching active site parsers failed")

    for site_parser_id in site_parser_ids:
        pass
        parse_news_list_task.delay(site_parser_id)
    return dict(result='SUCCESS', comment="Added tasks for starting {} site parsers".format(len(site_parser_ids)))
