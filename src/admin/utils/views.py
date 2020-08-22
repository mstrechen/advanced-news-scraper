from flask import url_for
from flask_admin.contrib import sqla
from flask_security import current_user
from werkzeug.utils import redirect


class PatchedModelView(sqla.ModelView):
    CONFIG_MODEL = None
    CONFIG_NAME = None
    CONFIG_CATEGORY = None

    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('security.login'))

    def __init__(self, session,
                 name=None, category=None, endpoint=None, url=None, static_folder=None,
                 menu_class_name=None, menu_icon_type=None, menu_icon_value=None, model=None):
        super(PatchedModelView, self).__init__(
            model=model or self.CONFIG_MODEL,
            session=session,
            name=name or self.CONFIG_NAME,
            category=category or self.CONFIG_CATEGORY,
            endpoint=endpoint,
            url=url,
            static_folder=static_folder,
            menu_class_name=menu_class_name,
            menu_icon_type=menu_icon_type,
            menu_icon_value=menu_icon_value,
        )
