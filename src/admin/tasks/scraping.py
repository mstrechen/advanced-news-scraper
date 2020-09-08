import logging

from admin import celery

logger = logging.getLogger(__name__)


@celery.task(queue='scraping')
def run_site_parsers():
    logger.info("Running site_parsers")
    return dict(result='SUCCESS', comment="Success!!!")
