from markupsafe import Markup

from admin.models.user import User
from admin.utils.views import PatchedModelView


def roles_formatter(view, context, model, name):
    roles = getattr(model, name)
    return Markup(''.join(
        f'<span class="badge badge-info">{role.name}</span>'
        for role in roles
    ))


class UsersView(PatchedModelView):
    CONFIG_MODEL = User
    can_delete = False
    can_view_details = True  # show a modal dialog with records details
    action_disallowed_list = ['delete', ]
    column_exclude_list = ['password', ]

    column_list = ['full_name', 'email', 'active', 'roles']
    column_editable_list = []
    form_edit_rules = ['full_name', 'email',]
    column_details_exclude_list = ['password']

    form_widget_args = {
        'id': {
            'readonly': True,
        },
        'roles': {
            'readonly': True,
        },
        'email': {
            'readonly': True,
        },
    }

    column_searchable_list = [
        'full_name',
        'email',
    ]
    column_formatters = {
        'roles': roles_formatter
    }
