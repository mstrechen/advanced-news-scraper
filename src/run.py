import os

from admin import app


def parse_bool(s: str):
    return s in ['1', 'T', 'true', 'True']


PORT = int(os.environ.get('PORT', '80'))
DEBUG = parse_bool(os.environ.get('DEBUG', False))

app.run(debug=DEBUG, port=PORT, host='0.0.0.0')
