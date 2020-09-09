import logging

from sqlalchemy.exc import SQLAlchemyError

from admin import celery
from admin.models.sites import Site
from admin.app import Session

from scraping import parse_news_list

logger = logging.getLogger(__name__)


def fetch_site_parser_ids():
    session = Session()
    site_parser_ids = session.query(Site.active_parser_id).all()
    session.close()

    return site_parser_ids


@celery.task(queue='test')
def run_site_parsers():
    try:
        site_parser_ids = fetch_site_parser_ids()
    except SQLAlchemyError:
        return dict(result='FAILURE', comment="Fetching active site parsers failed")

    for site_parser_id in site_parser_ids:
        parse_news_list.delay(site_parser_id)
    return dict(result='SUCCESS', comment="Added tasks for starting {} site parsers".format(len(site_parser_ids)))