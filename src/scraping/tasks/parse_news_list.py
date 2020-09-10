from selenium.common.exceptions import WebDriverException

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
    if site_parser.syntax == "json":
        rules = json.loads(site_parser.rules)
    else:
        raise ValueError("Yaml parser configuration isn't supported yet")

    list_rules = rules['list']
    list_url = list_rules['url']

    item_rules = list_rules['item']
    item_xpath = item_rules['xpath']

    item_link_subpath = item_rules['link_subpath']
    next_xpath = list_rules['next']

    article_rules = rules['article']

    return list_url, item_xpath, item_link_subpath, next_xpath, article_rules


def does_article_exist(link):
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
        return dict(result='SUCCESS', comment="Nothing to parse with site parser {}".format(site_parser_id))

    try:
        list_url, item_xpath, item_link_subpath, next_xpath, article_rules = parse_config(site_parser)
    except ValueError:
        return dict(result='FAILURE', comment="Error have occurred during parsing rules for site parser {}"
                    .format(site_parser_id))

    driver = get_driver()

    limit = 10

    next_url = list_url
    fetched_articles = 0
    reached_parsed_article = False
    has_next_page = True
    while fetched_articles < limit and has_next_page:
        try:
            page = driver.get(next_url)
        except WebDriverException:
            return dict(result='FAILURE', comment="Failed to get ".format(next_url))

        try:
            next_url = driver.find_element_by_xpath(next_xpath).get_attribute("href")
        except WebDriverException:
            has_next_page = False

        try:
            news_items = driver.find_elements_by_xpath(item_xpath)
        except WebDriverException:
            return dict(result='FAILURE', comment="Failed to get news items")

        for item in news_items:
            try:
                link = item.find_element(By.XPATH, ".//" + item_link_subpath).get_attribute("href")
            except WebDriverException:
                logger.info("Failed to extract article link from news list item")
                continue

            reached_parsed_article |= does_article_exist(link)
            if reached_parsed_article:
                break

            parse_article_task.delay(link, article_rules)

            fetched_articles += 1
            if fetched_articles == limit:
                break

        if reached_parsed_article or fetched_articles == limit:
            break
