import babel
from flask_admin import AdminIndexView
from flask_login import current_user

from admin.app import app, db
from admin.models.user import User
from flask import send_file

import flask_admin as admin

from admin.utils import url_tools
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

admin.add_view(UsersView(User, db.session, name='Users'))
