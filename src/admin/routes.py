import babel
from flask_admin import AdminIndexView
from flask_admin.babel import lazy_gettext
from flask_admin.consts import ICON_TYPE_GLYPH
from flask_login import current_user

from admin.app import app, db
from flask import send_file

import flask_admin as admin

from admin.utils import url_tools
from admin.utils.setup import setup_menu
from admin.views.articles import ArticlesView
from admin.views.clasterization.tag_rules import TagRulesView
from admin.views.clasterization.tags import TagsView
from admin.views.sites.site_parsers import SiteParsersView
from admin.views.sites.sites import SitesView
from admin.views.users import UsersView


@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')


@app.context_processor
def add_contexts():
    return dict(
        babel=babel,
        url_tools=url_tools,
        current_user=current_user,
    )


admin = admin.Admin(
    app, name='Advanced news scraper', template_mode='bootstrap3',
    index_view=AdminIndexView(template='index.html', url='/')
)

MENU = [
    (lazy_gettext('Users'), UsersView),
    (lazy_gettext('Sites'), [
        (lazy_gettext('Sites'), SitesView),
        (lazy_gettext('Site parsers'), SiteParsersView),
    ]),
    (lazy_gettext('Articles'), ArticlesView, {
        'menu_icon_type': ICON_TYPE_GLYPH, 'menu_icon_value': 'glyphicon-folder-open'
    }),
    (lazy_gettext('Tags'), [
        (lazy_gettext('Tags'), TagsView),
        (lazy_gettext('Tag rules'), TagRulesView),
    ]),
]


setup_menu(admin, db, MENU)
