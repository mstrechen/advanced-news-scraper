from admin.models.tags import Tag
from admin.utils.views import PatchedModelView


class TagsView(PatchedModelView):
    CONFIG_MODEL = Tag

    can_view_details = True

    column_editable_list = []
    can_create = False
    can_delete = False
    can_edit = False
