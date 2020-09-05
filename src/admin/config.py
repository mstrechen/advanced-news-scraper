import os

from celery.schedules import crontab


def parse_bool(s: str):
    return s in ['1', 'T', 'true', 'True', True]


def parse_list(s: str, default=None):
    if not s:
        return default or []
    return s.split(';')


DEBUG = os.environ.get('DEBUG')

FLASK_ADMIN_SWATCH = 'yeti'
SUPPORTED_LANGUAGES = ['en', 'uk']

# Create dummy secrey key so we can use sessions
SECRET_KEY = os.environ.get('SECRET_KEY', '123456790')


MYSQL_DATABASE_HOST = os.environ.get('MYSQL_HOST', 'mysql')
MYSQL_DATABASE_PORT = os.environ.get('MYSQL_PORT', 3306)
MYSQL_DATABASE_USER = os.environ.get('MYSQL_USER')
MYSQL_DATABASE_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DATABASE_DB = os.environ.get('MYSQL_DATABASE', 'news_scraper')

SQLALCHEMY_DATABASE_URI = \
    f'mysql+mysqldb://{MYSQL_DATABASE_USER}:{MYSQL_DATABASE_PASSWORD}' \
    f'@{MYSQL_DATABASE_HOST}:{MYSQL_DATABASE_PORT}/{MYSQL_DATABASE_DB}' \
    f'?charset=utf8mb4'


_BROKER_SCHEME = 'amqp'
_BROKER_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
_BROKER_PASSWORD = os.environ.get('RABBITMQ_DEFAULT_PASS')
_BROKER_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
_BROKER_PORT = int(os.environ.get('RABBITMQ_PORT', 5672))
_BROKER_VHOST = os.environ.get('RABBITMQ_VHOST', '/')

BROKER_URL = f'{_BROKER_SCHEME}://{_BROKER_USER}:{_BROKER_PASSWORD}@{_BROKER_HOST}:{_BROKER_PORT}/{_BROKER_VHOST}'

CELERY_RESULT_BACKEND = \
    f'db+mysql://{MYSQL_DATABASE_USER}:{MYSQL_DATABASE_PASSWORD}' \
    f'@{MYSQL_DATABASE_HOST}:{MYSQL_DATABASE_PORT}/{MYSQL_DATABASE_DB}'
CELERY_IMPORTS = 'admin.tasks'

CELERYBEAT_SCHEDULE = {
    'tasks.test_tasks.ping_host': {
        'task': 'admin.tasks.test_tasks.ping_host',
        'schedule': crontab(minute='0', hour='*/2')
    }
}

SQLALCHEMY_ECHO = parse_bool(os.environ.get('SQLALCHEMY_ECHO'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING')
LOGSTASH_HOST = os.environ.get('LOGSTASH_HOST')
LOGSTASH_PORT = int(os.environ.get('LOGSTASH_PORT', 0))
LOGSTASH_LOGLEVEL = os.environ.get('LOGSTASH_LOGLEVEL', 'INFO')

FORCE_HTTPS = not DEBUG and parse_bool(os.environ.get('FORCE_HTTPS', True))
CONTENT_SECURITY_POLICY = {}  # https://github.com/GoogleCloudPlatform/flask-talisman#options

SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'somesalt')
SECURITY_REGISTERABLE = parse_bool(os.environ.get('SECURITY_REGISTERABLE', True))
SECURITY_SEND_REGISTER_EMAIL = parse_bool(os.environ.get('SECURITY_SEND_REGISTER_EMAIL', False))
