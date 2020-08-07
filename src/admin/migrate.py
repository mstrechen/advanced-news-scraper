from admin.app import app, db


# TODO: flask-migrate instead of this
def migrate():
    with app.app_context():
        db.create_all()
