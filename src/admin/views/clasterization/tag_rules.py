import json

from flask_security import current_user
from flask_wtf import Form
from wtforms import ValidationError, HiddenField
import wtforms.validators as validators

from admin.models.tag_rules import TagRule
from admin.utils.views import PatchedModelView


class RuleQueryValidator:
    @classmethod
    def validate_rule(cls, rule):
        if type(rule) is str:
            return
        if type(rule) is list:
            for child_rule in rule:
                cls.validate_rule(child_rule)
        elif type(rule) is dict:
            if 'keywords' in rule:
                if type(rule['keywords']) is not list:
                    raise ValueError("Keywords should be a list")
                for keyword in rule['keywords']:
                    cls.validate_rule(keyword)
                if type(rule.get('min_count', 1)) is not int:
                    raise ValueError("min_count should be an int")
            else:
                if 'synonyms' not in rule:
                    raise ValueError('Missing "synonyms" or "keywords" field')
                cls.validate_rule(rule['synonyms'])
                if 'antonyms' in rule:
                    cls.validate_rule(rule['antonyms'])
        else:
            raise ValueError("Unexpected rule type: ", type(rule))

    @classmethod
    def validator(cls, form, field):
        try:
            rule = field.data
            rule = json.loads(rule)
            cls.validate_rule(rule)
        except Exception as e:
            raise ValidationError(*e.args)


class TagRulesView(PatchedModelView):
    CONFIG_MODEL = TagRule

    can_view_details = True

    column_editable_list = []
    can_create = True
    can_delete = False
    can_edit = False
    column_filters = ['rule_type']

    form_args = {
        'rule_query': dict(validators=[RuleQueryValidator.validator]),
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
