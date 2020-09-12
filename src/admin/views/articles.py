from flask_admin.tools import rec_getattr

from admin.models.articles import Article
from admin.utils.views import PatchedModelView


class ArticlesView(PatchedModelView):
    CONFIG_MODEL = Article
    can_view_details = True

    column_editable_list = []
    can_delete = False
    can_create = False
    can_edit = False

    column_list = ['site_id', 'language', 'url', 'text.title', 'text.content']
    column_details_list = column_list
    column_formatters = {
        'text.content': lambda c, v, m, n: rec_getattr(m, n, '')[:300]
    }
    column_formatters_detail = {}
