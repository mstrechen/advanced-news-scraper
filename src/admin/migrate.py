from flask import app

from time import sleep

from sqlalchemy.exc import OperationalError

from admin.app import app, db


def try_to_migrate(wait_before_attempt=5):
    sleep(wait_before_attempt)
    try:
        db.create_all()
        return True
    except OperationalError:
        return False


# TODO: flask-migrate instead of this
def migrate(max_retries=12, wait_for_attempt=5):
    with app.app_context():
        if not any(try_to_migrate(wait_for_attempt) for _ in range(max_retries)):
            raise Exception("Failed to migrate after %s seconds", max_retries * wait_for_attempt)
    app.logger.info("Successfully migrated!")
