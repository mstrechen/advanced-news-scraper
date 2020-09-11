from flask_security import current_user
from flask_wtf import Form
from wtforms import ValidationError, HiddenField
import wtforms.validators as validators

from admin.models.tag_rules import TagRule
from admin.utils.views import PatchedModelView
from clasterization.query_translator import QueryDecodeError, QueryTranslator


def rule_query_validator(form, field):
    try:
        # TODO: make separate validator
        QueryTranslator(field.data).translate().to_dict()
    except QueryDecodeError as e:
        raise ValidationError(' '.join(map(str, e.args))) from e


class TagRulesView(PatchedModelView):
    CONFIG_MODEL = TagRule

    can_view_details = True

    column_editable_list = []
    can_create = True
    can_delete = False
    can_edit = False
    column_filters = ['rule_type']

    form_args = {
        'rule_query': dict(validators=[rule_query_validator]),
        'enabled_timestamp': dict(validators=[validators.optional()]),
        'disabled_timestamp': dict(validators=[validators.optional()]),
    }
    form_excluded_columns = ['creator']

    form_choices = {
        'rule_type': [
            ('es_query', 'es_query'),
            ('keyword_list', 'keyword_list'),
        ],
        # TODO: autogenerate
        'rule_language': [
            ('uk', 'uk'),
            ('en', 'en'),
            ('ru', 'ru'),
        ]
    }

    def get_create_form(self):
        form = super(TagRulesView, self).get_create_form()

        class Form(form):
            creator_id = HiddenField()

        return Form

    def create_model(self, form: Form):
        form.creator_id.data = current_user.id
        return super(TagRulesView, self).create_model(form)
