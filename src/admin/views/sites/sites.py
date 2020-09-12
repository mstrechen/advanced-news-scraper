import requests

from wtforms import ValidationError

from admin.models.sites import Site
from admin.utils.views import PatchedModelView


class UrlAvailabilityValidator:
    @classmethod
    def validator(cls, form, field):
        try:
            url = field.data
            resp = requests.head(url)
            resp.raise_for_status()
        except Exception:
            raise ValidationError("Provided invalid or inaccessible URL")

class SitesView(PatchedModelView):
    CONFIG_MODEL = Site

    can_view_details = True

    column_editable_list = []
    can_create = True
    can_delete = True

    form_args = {
        'base_url': dict(validators=[UrlAvailabilityValidator.validator]),
    }
    form_excluded_columns = ['created']
