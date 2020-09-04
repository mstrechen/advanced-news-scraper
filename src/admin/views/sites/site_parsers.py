from admin.models.site_parsers import SiteParser
from admin.utils.views import PatchedModelView


class SiteParsersView(PatchedModelView):
    CONFIG_MODEL = SiteParser

    can_view_details = True

    column_editable_list = []
    can_create = False
    can_delete = False
