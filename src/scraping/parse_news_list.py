from admin import celery


@celery.task(queue='test')
def parse_news_list(site_parse_id):
    pass
