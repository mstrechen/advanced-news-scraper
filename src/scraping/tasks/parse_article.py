import json
from json import JSONDecodeError

from selenium.common.exceptions import WebDriverException

import logging

from admin.app import app, db, celery
from admin.models.articles import ArticleText
from scraping import get_driver

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def save_article_text(parser_id, article_id, title, text):
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


def get_pure_text(text):
    return BeautifulSoup(text, "lxml").text


def parse_article(link, article_rules, article_id, site_parser_id, dry_run):
    if article_rules is None:
        return dict(result='FAILURE', comment="Failed to parse page {}, parsing rules for article aren't specified"
                    .format(link))

    logger.info("Parsing article by link {}".format(link))

    driver = get_driver()

    try:
        driver.get(link)
    except WebDriverException:
        return dict(result='FAILURE', comment="Failed to get page {}".format(link))

    text_xpath, title_xpath = parse_config(article_rules)

    try:
        element_text = driver.find_element_by_xpath(text_xpath)
    except WebDriverException:
        return dict(result='FAILURE', comment="Failed to get element text of article {} by xpath {}"
                    .format(link, text_xpath))

    try:
        element_title = driver.find_element_by_xpath(title_xpath)
    except WebDriverException:
        return dict(result='FAILURE', comment="Failed to get element title of article {} by xpath {}"
                    .format(link, title_xpath))

    text = get_pure_text(element_text.get_attribute("outerHTML"))
    title = get_pure_text(element_title.get_attribute("outerHTML"))

    if not dry_run:
        save_article_text(site_parser_id, article_id, title, text)

    return dict(result='SUCCESS', comment="Successfully parsed article {}".format(link),
                article={"text": text, "title": title})


def parse_article_dry_run(link, rules):
    logger.info("received link {} rules {}".format(link, rules))
    try:
        rules = json.loads(rules)
    except JSONDecodeError:
        return dict(result="FAILURE", comment="Error during parsing provided json {}".format(rules))
    return parse_article(link, rules['article'], None, None, True)


@celery.task(queue='articles')
def parse_article_task(link, article_rules, article_id, site_parser_id):
    return parse_article(link, article_rules, article_id, site_parser_id, False)
