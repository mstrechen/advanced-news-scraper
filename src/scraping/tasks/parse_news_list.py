from admin import celery
from admin.models.site_parsers import SiteParser
from admin.models.articles import Article
from admin.app import Session

from scraping import get_driver
from scraping.tasks.parse_article import parse_article_task
from selenium.webdriver.common.by import By

import json
import logging

logger = logging.getLogger(__name__)


def fetch_site_parser_by_id(site_parser_id):
    session = Session()
    site_parser = session.query(SiteParser).filter_by(parser_id=site_parser_id)[0]
    session.close()

    return site_parser


def parse_config(site_parser):
    logger.info(site_parser.rules)
    if site_parser.syntax == "json":
        rules = json.loads(site_parser.rules)
    else:
        raise Exception("Yaml parser configuration isn't supported yet")

    list_rules = rules['list']
    list_url = list_rules['url']

    item_rules = list_rules['item']
    item_xpath = item_rules['xpath']

    item_link_subpath = item_rules['link_subpath']
    next_xpath = list_rules['next']

    article_rules = rules['article']

    return list_url, item_xpath, item_link_subpath, next_xpath, article_rules


def is_article_exists(link):
    session = Session()
    article_exists = session.query(Article).filter_by(url=link).count() > 0
    session.close()

    return article_exists


@celery.task(queue='test')
def parse_news_list_task(site_parser_id):
    pass
    logger.info("Parsing news list for site parser {}".format(site_parser_id))
    site_parser = fetch_site_parser_by_id(site_parser_id)
    if not site_parser.has_newslist_parser:
        return dict(result='SUCCESS', comment="Nothing to parse with site parser {}".format(site_parser.parser_id))

    list_url, item_xpath, item_link_subpath, next_xpath, article_rules = parse_config(site_parser)

    driver = get_driver()

    next_url = list_url
    fetched_articles = 0
    reached_parsed_article = False
    limit = 10
    while fetched_articles < limit:
        page = driver.get(next_url)
        next_url = driver.find_element_by_xpath(next_xpath).get_attribute("href")

        news_items = driver.find_elements_by_xpath(item_xpath)
        for item in news_items:
            link = item.find_element(By.XPATH, ".//" + item_link_subpath).get_attribute("href")

            reached_parsed_article |= is_article_exists(link)
            if reached_parsed_article:
                break

            parse_article_task.delay(link, article_rules)

            fetched_articles += 1
            if fetched_articles == limit:
                break

        if reached_parsed_article or fetched_articles == limit:
            break
