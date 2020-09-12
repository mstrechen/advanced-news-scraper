import logging

from sqlalchemy.exc import SQLAlchemyError

from admin import celery
from admin.models.site_parsers import SiteParser
from admin.app import db, app

from scraping.tasks.parse_news_list import parse_news_list_task

logger = logging.getLogger(__name__)


def fetch_site_parser_ids():
    with app.app_context():
        site_parser_ids = db.session.query(SiteParser.parser_id) \
            .filter(SiteParser.active.is_(True)).all()

    return site_parser_ids


@celery.task(queue='site_parsers')
def run_site_parsers_task():
    try:
        site_parser_ids = fetch_site_parser_ids()
    except SQLAlchemyError:
        return dict(result='FAILURE', comment="Fetching active site parsers failed")

    for site_parser_id in site_parser_ids:
        parse_news_list_task.delay(site_parser_id)
    return dict(result='SUCCESS', comment="Added tasks for starting {} site parsers".format(len(site_parser_ids)))
