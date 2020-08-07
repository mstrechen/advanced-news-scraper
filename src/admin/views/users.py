from flask_admin.contrib import sqla


class UsersView(sqla.ModelView):
    can_view_details = True  # show a modal dialog with records details
    action_disallowed_list = ['delete', ]

    form_widget_args = {
        'id': {
            'readonly': True
        }
    }
    column_searchable_list = [
        'full_name',
        'email',
    ]
    column_editable_list = ['full_name', ]

