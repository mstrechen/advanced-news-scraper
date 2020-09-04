from admin.models.articles import Article
from admin.utils.views import PatchedModelView


class ArticlesView(PatchedModelView):
    CONFIG_MODEL = Article
    can_view_details = True

    column_editable_list = []
    can_delete = False
    can_create = False
    can_edit = False
