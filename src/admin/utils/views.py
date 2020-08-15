from flask import url_for
from flask_security import current_user
from werkzeug.utils import redirect


class ProtectedView:
    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))
