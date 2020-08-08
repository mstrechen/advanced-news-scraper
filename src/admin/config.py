import os


def parse_bool(s: str):
    return s in ['1', 'T', 'true', 'True']


FLASK_ADMIN_SWATCH = 'yeti'
SUPPORTED_LANGUAGES = ['en', 'uk']

# Create dummy secrey key so we can use sessions
SECRET_KEY = os.environ.get('SECRET_KEY', '123456790')


MYSQL_DATABASE_HOST = os.environ.get('MYSQL_HOST', 'mysql')
MYSQL_DATABASE_PORT = os.environ.get('MYSQL_PORT', 3306)
MYSQL_DATABASE_USER = os.environ.get('MYSQL_USER')
MYSQL_DATABASE_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DATABASE_DB = os.environ.get('MYSQL_DB', 'news_scraper')


SQLALCHEMY_DATABASE_URI = \
    f'mysql+mysqldb://{MYSQL_DATABASE_USER}:{MYSQL_DATABASE_PASSWORD}' \
    f'@{MYSQL_DATABASE_HOST}:{MYSQL_DATABASE_PORT}/{MYSQL_DATABASE_DB}' \
    f'?charset=utf8mb4'

SQLALCHEMY_ECHO = parse_bool(os.environ.get('SQLALCHEMY_ECHO'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING')
