from admin.app import app, db
from admin.models.user import User
from flask import Markup, send_file

import flask_admin as admin

# Flask views
from admin.views.users import UsersView


@app.route('/')
def index():
    tmp = u"""
<p><a href="/admin/?lang=en">Click me to get to Admin! (English)</a></p>
<p><a href="/admin/?lang=en">Натисни, щоб увійти в Адмінку! (Українською)</a></p>
"""
    return tmp


@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')


admin = admin.Admin(app, name='Advanced news scraper', template_mode='bootstrap3')

admin.add_view(UsersView(User, db.session, name='Users'))