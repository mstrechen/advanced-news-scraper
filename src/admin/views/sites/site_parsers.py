from flask_wtf import Form
from flask_security import current_user
from wtforms import HiddenField

from admin.models.site_parsers import SiteParser
from admin.utils.views import PatchedModelView


class SiteParsersView(PatchedModelView):
    CONFIG_MODEL = SiteParser

    can_view_details = True

    column_editable_list = []
    can_create = True
    can_edit = True
    can_delete = False

    form_excluded_columns = ['has_newslist_parser', 'has_article_parser', 'creator_id', 'created']
    form_choices = {
        'syntax': [
            ('json', 'json'),
            # ('yaml', 'yaml'),
        ],
        'type': [
            ('dynamic', 'dynamic'),
            # ('static', 'static'),
            # ('rest_api', 'rest_api'),
        ],
    }

    def get_create_form(self):
        form = super(SiteParsersView, self).get_create_form()

        class Form(form):
            has_newslist_parser = HiddenField()
            has_article_parser = HiddenField()
            creator_id = HiddenField()

        return Form

    def create_model(self, form: Form):
        form.has_newslist_parser.data = True
        form.has_article_parser = True
        form.creator_id.data = current_user.id
        return super(SiteParsersView, self).create_model(form)
