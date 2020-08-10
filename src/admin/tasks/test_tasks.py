import logging

import requests

from admin import celery

logger = logging.getLogger(__name__)


@celery.task(queue='test')
def ping_host(host='http://chytalka.space'):
    logger.info("Task ping_host started with host %s", host)
    res = requests.get(host)
    if res.status_code == 200:
        logger.info("Successfully pinged %s", host)
        return dict(result='SUCCESS', comment="Success!!!")
    else:
        logger.error("Resource %s unavailable", host)
        return dict(result='FAILED', comment="Failed!!!!")
