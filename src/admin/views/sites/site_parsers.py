import json

from lxml import etree
from flask import jsonify, request
from flask_wtf import Form
from flask_security import current_user
from flask_admin import expose
from wtforms import HiddenField, ValidationError

from admin.models.site_parsers import SiteParser
from admin.utils.views import PatchedModelView

from scraping.tasks.parse_news_list import parse_news_list_dry_run
from scraping.tasks.parse_article import parse_article_dry_run


def _is_valid_xpath(xpath):
    fake_tree = etree.fromstring("<html></html>")
    try:
        fake_tree.xpath(xpath)
        return True
    except Exception:
        return False


def check_has_newslist_parser(form):
    if form.syntax.data == 'json':
        try:
            rules = form.rules.data
            rules = json.loads(rules)
            return rules.get('list') is not None
        except ValueError:
            return False
    else:
        return True


def check_has_article_parser(form):
    if form.syntax.data == 'json':
        try:
            rules = form.rules.data
            rules = json.loads(rules)
            return rules.get('article') is not None
        except ValueError:
            return False
    else:
        return True


def parser_rules_validator(form, field):
    try:
        form_rule_syntax = form.syntax.data
        form_base_url = form.site.data.base_url

        rules = field.data
        if form_rule_syntax == 'json':
            rules = json.loads(rules)
            rule_lang = rules.get('lang')
            if rule_lang is None:
                raise KeyError('lang')
            # consider having global var with languages
            if rule_lang not in ['uk', 'ru', 'en']:
                raise ValueError("lang", "be one of uk, ru, en")
            list_rules = rules.get('list')

            if list_rules is not None:
                if not isinstance(list_rules, dict):
                    raise ValueError('list', 'be a JSON object')

                url = list_rules.get('url')
                if url is None:
                    raise KeyError('url', 'list')
                if not url.startswith(form_base_url):
                    raise ValueError('url', 'start with url of chosen site')

                item = list_rules.get('item')
                if item is None:
                    raise KeyError('item', 'list')
                if not isinstance(item, dict):
                    raise ValueError('list.item', 'be a JSON object')

                xpath = item.get('xpath')
                if xpath is None:
                    raise KeyError('xpath', 'list.item')
                if not _is_valid_xpath(xpath):
                    raise ValueError('list.item.xpath', 'be a valid XPath')

                link_subpath = item.get('link_subpath')
                if link_subpath is None:
                    raise KeyError('link_subpath', 'list.item')
                if not _is_valid_xpath(link_subpath):
                    raise ValueError('list.item.link_subpath', 'be a valid XPath')

                next = list_rules.get('next')
                if next is None:
                    raise KeyError('next', 'list')
                if not _is_valid_xpath(next):
                    raise ValueError('list.next', 'be a valid XPath')

            article = rules.get('article')
            if article is not None:
                if not isinstance(article, dict):
                    raise ValueError('article', 'be a JSON object')
                text_xpath = article.get('text_xpath')
                if text_xpath is None:
                    raise KeyError('text_xpath', 'article')
                if not _is_valid_xpath(text_xpath):
                    raise ValueError('article.text_xpath', 'be a valid XPath')

                title_xpath = article.get('text_xpath')
                if title_xpath is None:
                    raise KeyError('title_xpath', 'article')
                if not _is_valid_xpath(text_xpath):
                    raise ValueError('article.title_xpath', 'be a valid XPath')

        if form_rule_syntax == 'yaml':
            raise ValueError('Syntax is %s' % form_rule_syntax)
    except ValueError as e:
        if len(e.args) == 2:
            raise ValidationError('Value of field "%s" should %s' % (e.args[0], e.args[1]))
        else:
            raise ValidationError(e.args[0])
    except KeyError as e:
        if len(e.args) == 1:
            raise ValidationError('High-level key "%s" is necessary' % e.args[0])
        else:
            raise ValidationError('Key "%s" in "%s" object is necessary' % (e.args[0], e.args[1]))


class SiteParsersView(PatchedModelView):
    CONFIG_MODEL = SiteParser

    edit_template = 'scraping/site_parsers.edit.html'
    create_template = 'scraping/site_parsers.new.html'

    can_view_details = True

    column_editable_list = []
    can_create = True
    can_edit = True
    can_delete = True

    form_excluded_columns = ['has_newslist_parser', 'has_article_parser', 'creator_id', 'created']
    form_choices = {
        'syntax': [
            ('json', 'json'),
            # ('yaml', 'yaml'),
        ],
        'type': [
            ('dynamic', 'dynamic'),
            # ('static', 'static'),
            # ('rest_api', 'rest_api'),
        ],
    }
    form_args = {
        'rules': dict(validators=[parser_rules_validator],
                      render_kw=dict(rows="20")),
    }

    def get_create_form(self):
        form = super(SiteParsersView, self).get_create_form()

        class Form(form):
            has_newslist_parser = HiddenField()
            has_article_parser = HiddenField()
            creator_id = HiddenField()

        return Form

    def create_model(self, form: Form):
        form.has_newslist_parser.data = check_has_newslist_parser(form)
        form.has_article_parser.data = check_has_article_parser(form)
        form.creator_id.data = current_user.id
        return super(SiteParsersView, self).create_model(form)

    @expose('/edit/debug', methods=('POST', ))
    @expose('/new/debug', methods=('POST', ))
    def debug_view(self):
        data = request.get_data()
        result = parse_news_list_dry_run(data)
        if result['result'] == 'SUCCESS':
            return jsonify(ok=result['comment'], fetched_articles=result['fetched_articles'])
        else:
            return jsonify(error="", safe_error=result['comment'], fetched_articles=result['fetched_articles'])

    @expose('/edit/debug_article', methods=('POST', ))
    @expose('/new/debug_article', methods=('POST', ))
    def debug_article_view(self):
        data = json.loads(request.get_data())
        result = parse_article_dry_run(data["link"], data["rules"])
        if result['result'] == 'SUCCESS':
            return jsonify(ok=result['comment'], article=result['article']), 200
        else:
            return jsonify(error="", safe_error=result['comment']), 400
