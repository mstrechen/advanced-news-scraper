from celery import Celery
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

    app.logger.setLevel(app.config['LOGLEVEL'])


def _init_flask_security(app, db, admin):
    from admin.models.user import User, UserRole
    user_datastore = SQLAlchemyUserDatastore(db, User, UserRole)
    security = Security(app, user_datastore, register_form=RegisterForm)  #noqa

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )


@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override and override in app.config['SUPPORTED_LANGUAGES']:
        session['lang'] = override

    return session.get('lang', 'en')


from admin.routes import admin as Admin # noqa: E402, F401
init_app(Admin)
