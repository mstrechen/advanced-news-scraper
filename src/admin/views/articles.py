from flask_admin.tools import rec_getattr

from admin.models.articles import Article
from admin.utils.views import PatchedModelView


def tags_formatter(view, context, model, name):
    for tag in model.tags:
        print(tag, flush=True)
    return 'WOW'
    # roles = getattr(model, name)
    # return Markup(''.join(
    #     f'<span class="badge badge-info">{role.name}</span>'
    #     for role in roles
    # ))


class ArticlesView(PatchedModelView):
    CONFIG_MODEL = Article
    can_view_details = True

    column_editable_list = []
    can_delete = False
    can_create = False
    can_edit = False

    column_list = ['site_id', 'language', 'url', 'text.title', 'text.content', 'tags']
    column_details_list = column_list
    column_formatters = {
        'text.content': lambda c, v, m, n: rec_getattr(m, n, '')[:300],
    }
    column_formatters_detail = {}

    def get_query(self):
        return super(ArticlesView, self) \
            .get_query() \
            .filter(Article.last_text_id.isnot(None))  # noqa

    def get_count_query(self):
        return super(ArticlesView, self) \
            .get_count_query() \
            .filter(Article.last_text_id.isnot(None))  # noqa
