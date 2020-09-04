from admin.models.tag_rules import TagRule
from admin.utils.views import PatchedModelView


class TagRulesView(PatchedModelView):
    CONFIG_MODEL = TagRule

    can_view_details = True

    column_editable_list = []
    can_create = False
    can_delete = False
    can_edit = False
