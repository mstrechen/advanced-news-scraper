from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy()
babel = Babel()


def init_app():
    db.init_app(app)
    babel.init_app(app)
    app.logger.setLevel(app.config['LOGLEVEL'])


@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'en')


import admin.routes
init_app()
