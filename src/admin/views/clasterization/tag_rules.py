from elasticsearch_dsl import Search
from flask import request, jsonify
from flask_admin import expose
from flask import escape
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
        QueryTranslator(field.data, form.rule_language.data).translate().to_dict()
    except QueryDecodeError as e:
        raise ValidationError(' '.join(map(str, e.args))) from e


class TagRulesView(PatchedModelView):
    CONFIG_MODEL = TagRule

    edit_template = 'clasterization/tag_rules.edit.html'
    create_template = 'clasterization/tag_rules.new.html'

    can_view_details = True

    column_editable_list = []
    can_create = True
    can_delete = False
    can_edit = True
    column_filters = ['rule_type']

    form_args = {
        'rule_query': dict(validators=[rule_query_validator]),
        'enabled_timestamp': dict(validators=[validators.optional()]),
        'disabled_timestamp': dict(validators=[validators.optional()]),
    }
    form_excluded_columns = ['creator']

    form_choices = {
        'rule_type': [
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

    @expose('/edit/debug', methods=('POST', ))
    @expose('/new/debug', methods=('POST', ))
    def debug_view(self):
        try:
            data = request.get_data()
            query = QueryTranslator(data).translate()
            res = [
                dict(**article.to_dict(), id=article.meta.id)
                for article in Search(index='article_texts').query(query)
            ]
            return jsonify(ok='ok', hits=res)
        except QueryDecodeError as e:
            error = ' '.join(map(str, e.args))
            safe_error = escape(error)
            return jsonify(error=error, safe_error=safe_error), 400
