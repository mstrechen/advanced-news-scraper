from admin.models.sites import SiteParser
from admin.utils.views import ProtectedView


class SiteParsersView(ProtectedView):
    CONFIG_MODEL = SiteParser

    can_view_details = True

    column_editable_list = []
    can_create = False
    can_delete = False
