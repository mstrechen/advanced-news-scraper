from admin.models.sites import Site
from admin.utils.views import ProtectedView


class SitesView(ProtectedView):
    CONFIG_MODEL = Site

    can_view_details = True

    column_editable_list = []
    can_create = False
    can_delete = False
