import babel
from flask_admin import AdminIndexView
from flask_admin.babel import lazy_gettext
from flask_login import current_user

from admin.app import app, db
from flask import send_file

import flask_admin as admin

from admin.utils import url_tools
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

admin.add_view(UsersView(db.session, name=lazy_gettext('Users')))
admin.add_view(SitesView(db.session, name=lazy_gettext('Sites'), category=lazy_gettext('Sites')))
admin.add_view(SiteParsersView(db.session, name=lazy_gettext('Site parsers'), category=lazy_gettext('Sites')))
