from selenium.common.exceptions import WebDriverException

from admin.models.site_parsers import SiteParser
from admin.models.articles import Article
from admin.app import app, db, celery

from scraping import get_driver
from scraping.tasks.parse_article import parse_article_task
from selenium.webdriver.common.by import By

import json
import logging
import collections

logger = logging.getLogger(__name__)

Config = collections.namedtuple('Config', 'lang list_url item_xpath item_link_subpath next_xpath article_rules')


def fetch_site_parser_by_id(site_parser_id):
    with app.app_context():
        site_parser = db.session.query(SiteParser).filter_by(parser_id=site_parser_id)[0]
    return site_parser


def parse_config(rules_str, syntax):
    if syntax == "json":
        rules = json.loads(rules_str)
    else:
        raise ValueError("Yaml parser configuration isn't supported yet")

    lang = rules['lang']

    list_rules = rules['list']
    list_url = list_rules['url']

    item_rules = list_rules['item']
    item_xpath = item_rules['xpath']

    item_link_subpath = item_rules['link_subpath']
    next_xpath = list_rules['next']

    article_rules = rules['article']

    return Config(lang, list_url, item_xpath, item_link_subpath, next_xpath, article_rules)


def article_exists(link, filter_has_text=False):
    with app.app_context():
        query = db.session.query(Article).filter_by(url=link)
        if filter_has_text:
            query = query.filter(Article.last_text_id.isnot(None))
        return query.count() > 0


def get_article_by_url(link):
    with app.app_context():
        return Article.query.filter_by(url=link).first().article_id


def save_article(site_id, lang, url):
    logger.info('Adding article to database {}'.format(url))

    with app.app_context():
        article = Article(site_id=site_id, language=lang, url=url)
        db.session.add(article)
        db.session.commit()
        article_id = article.article_id

    return article_id


def fetch_and_process_articles(config, site_parser, dry_run):
    driver = get_driver()

    limit = 30

    next_url = config.list_url
    fetched_articles = []
    has_next_page = True
    while len(fetched_articles) < limit and has_next_page:
        try:
            driver.get(next_url)
        except WebDriverException:
            logger.exception('Failed to get %s', next_url)
            return dict(result='FAILURE', comment="Failed to get {}".format(next_url))

        try:
            next_url = driver.find_element_by_xpath(config.next_xpath).get_attribute("href")
        except WebDriverException:
            has_next_page = False

        try:
            news_items = driver.find_elements_by_xpath(config.item_xpath)
        except WebDriverException:
            logger.exception('Failed to get news items')
            return dict(result='FAILURE', comment="Failed to get news items")

        for item in news_items:
            try:
                link = item.find_element(By.XPATH, ".//" + config.item_link_subpath).get_attribute("href")
            except WebDriverException:
                logger.info("Failed to extract article link from news list item", exc_info=True)
                continue

            fetched_articles.append(link)
            if len(fetched_articles) == limit:
                break

            if dry_run:
                continue

            if not article_exists(link, filter_has_text=True):
                # Saving article into database here, so we won't create another task for parsing same article
                if article_exists(link, filter_has_text=False):
                    article_id = get_article_by_url(link)
                else:
                    article_id = save_article(site_parser.site_id, config.lang, link)
                parse_article_task.delay(link, config.article_rules, article_id, site_parser.parser_id)

        if len(fetched_articles) == limit:
            break

    return dict(result='SUCCESS', comment="Successfully parsed news list with site parser",
                fetched_articles=fetched_articles)


def parse_news_list_dry_run(config_str):
    config = parse_config(config_str, "json")
    return fetch_and_process_articles(config, None, True)


@celery.task(queue='news_lists')
def parse_news_list_task(site_parser_id):
    logger.info("Parsing news list for site parser {}".format(site_parser_id))
    site_parser = fetch_site_parser_by_id(site_parser_id)

    if site_parser.type != 'dynamic':
        return dict(result='FAILURE', comment="Only dynamic news_list parsers are supported")

    if not site_parser.has_newslist_parser:
        return dict(result='SUCCESS', comment="Nothing to parse with site parser {}".format(site_parser_id))

    try:
        config = parse_config(site_parser.rules, site_parser.syntax)
    except ValueError:
        return dict(result='FAILURE', comment="Error have occurred during parsing rules for site parser {}"
                    .format(site_parser_id))

    return fetch_and_process_articles(config, site_parser, False)
