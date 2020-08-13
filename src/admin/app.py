from celery import Celery
from flask import Flask, request, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask_seasurf import SeaSurf
from flask_talisman import Talisman

app = Flask(__name__)
app.config.from_pyfile('config.py')

celery = Celery(app.name)
celery.conf.update(app.config)

db = SQLAlchemy()
babel = Babel()
migrate = Migrate()
csrf = SeaSurf()
talisman = Talisman()


def init_app():
    db.init_app(app)
    babel.init_app(app, )
    migrate.init_app(app, db)
    talisman.init_app(
        app, force_https=app.config['FORCE_HTTPS'],
        content_security_policy=app.config['CONTENT_SECURITY_POLICY']
    )

    app.logger.setLevel(app.config['LOGLEVEL'])


@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override and override in app.config['SUPPORTED_LANGUAGES']:
        session['lang'] = override

    return session.get('lang', 'en')


import admin.routes  # noqa: E402, F401
init_app()
