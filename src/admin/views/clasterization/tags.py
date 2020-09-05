from gettext import gettext
from typing import Optional

from flask import flash

from admin.models.tags import Tag
from admin.utils.views import PatchedModelView


class TagsView(PatchedModelView):
    CONFIG_MODEL = Tag

    can_view_details = True
    can_create = True
    can_delete = False
    can_edit = True

    form_edit_rules = ['name', 'parent_tag', ]
    column_list = ['name', 'parent_tag', 'full_name', ]
    form_create_rules = ['name', 'parent_tag', ]

    def update_model(self, form, model: Tag):
        new_parent: Optional[Tag] = form.parent_tag.data
        if new_parent:
            disallowed_ids_list = [tag.tag_id for tag in new_parent.parents_chain]
            if model.tag_id in disallowed_ids_list:
                flash(gettext("You try make tag its own (grand)child"))
                return False
        return super(TagsView, self).update_model(form, model)
