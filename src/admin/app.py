import logging

import logstash
from celery import Celery, signals
from flask import Flask, request, session, url_for
from flask_admin import helpers as admin_helpers
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask_seasurf import SeaSurf
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix

from admin.utils.forms import RegisterForm

app = Flask(__name__)
app.config.from_pyfile('config.py')

celery = Celery(app.name)
celery.conf.update(app.config)

db = SQLAlchemy()
babel = Babel()
migrate = Migrate()
csrf = SeaSurf()
talisman = Talisman()
app.wsgi_app = ProxyFix(app.wsgi_app)


def init_app(admin):
    db.init_app(app)
    babel.init_app(app, )
    migrate.init_app(app, db)
    talisman.init_app(
        app, force_https=app.config['FORCE_HTTPS'],
        content_security_policy=app.config['CONTENT_SECURITY_POLICY']
    )
    _init_flask_security(app, db, admin)
    _init_loggers(app)
    _init_es(app)

def _init_flask_security(app, db, admin):
    from admin.models.user import User, UserRole
    user_datastore = SQLAlchemyUserDatastore(db, User, UserRole)
    security = Security(app, user_datastore, register_form=RegisterForm)  # noqa

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )


def _init_loggers(app: Flask):
    app.logger.setLevel(app.config['LOGLEVEL'])
    logger = logging.getLogger()
    logger.setLevel(app.config['LOGLEVEL'])

    if app.config['LOGSTASH_HOST']:
        _init_logstash_handler(logger)


def _init_es(app: Flask):
    from admin.init_scripts.es import init_es
    init_es(app)


@signals.after_setup_logger.connect
def _init_logstash_handler(logger=None, loglevel=logging.DEBUG, **kwargs):
    handler = logstash.TCPLogstashHandler(
        app.config['LOGSTASH_HOST'],
        app.config['LOGSTASH_PORT'],
        version=1,
    )
    handler.setLevel(app.config['LOGSTASH_LOGLEVEL'])
    logger.addHandler(handler)
    return logger


@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override and override in app.config['SUPPORTED_LANGUAGES']:
        session['lang'] = override

    return session.get('lang', 'en')


from admin.routes import admin as Admin  # noqa: E402, F401
init_app(Admin)
