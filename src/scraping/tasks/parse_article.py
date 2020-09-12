from selenium.common.exceptions import WebDriverException

from admin import celery
import logging

from admin.app import app, db
from admin.models.articles import ArticleText
from scraping import get_driver

from lxml import etree
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def insert_article_text(parser_id, article_id, title, text):
    logger.info('Adding article text to database {}'.format(title))
    with app.app_context():
        hash_text = hash(text)
        article_text = ArticleText(parser_id=parser_id, article_id=article_id,
                                   title=title, content=text, hash=hash_text)
        db.session.add(article_text)
        db.session.commit()


def parse_config(article_rules):
    text_xpath = article_rules['text_xpath']
    title_xpath = article_rules['title_xpath']

    return text_xpath, title_xpath


def elem_to_str(elem):
    res = etree.tostring(elem, encoding='utf-8').decode('utf-8')
    for e in elem:
        res += etree.tostring(e, encoding='utf-8').decode('utf-8')
    return res.strip()


def get_pure_text(text):
    return BeautifulSoup(text, "lxml").text


@celery.task(queue='test')
def parse_article_task(link, article_rules, article_id, site_parser_id):
    if article_rules is None:
        return dict(result='FAILURE', comment="Failed to parse page {}, parsing rules for article aren't specified".format(link))

    logger.info("Parsing article by link {}".format(link))

    driver = get_driver()

    try:
        driver.get(link)
    except WebDriverException:
        return dict(result='FAILURE', comment="Failed to get page {}".format(link))

    text_xpath, title_xpath = parse_config(article_rules)

    try:
        element_text = driver.find_element_by_xpath(text_xpath)
        element_title = driver.find_element_by_xpath(title_xpath)
    except WebDriverException:
        return dict(result='FAILURE', comment="Failed to get elements of article {}".format(link))

    text = get_pure_text(element_text.get_attribute("outerHTML"))
    title = get_pure_text(element_title.get_attribute("outerHTML"))

    insert_article_text(site_parser_id, article_id, title, text)
    return dict(result='SUCCESS', comment="Successfully parsed article {}".format(link))
