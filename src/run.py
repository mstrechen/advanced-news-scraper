import os
import logging

from admin import app
from admin.migrate import migrate


def parse_bool(s: str):
    return s in ['1', 'T', 'true', 'True']


MODE = os.environ.get('MODE', 'WEB').upper()

if MODE == 'MIGRATE':
    migrate()
elif MODE == 'WEB':
    PORT = int(os.environ.get('PORT', '80'))
    DEBUG = parse_bool(os.environ.get('DEBUG', False))

    app.run(debug=DEBUG, port=PORT, host='0.0.0.0')
else:
    logging.error("Unknown MODE %s", MODE)
