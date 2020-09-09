from admin import celery
import logging

logger = logging.getLogger(__name__)


@celery.task(queue='test')
def parse_article_task(link, article_rules):
    logger.info("Parsing article by link {}".format(link))
    pass
