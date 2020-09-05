from typing import Generator

from admin.app import db


class Tag(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.INTEGER, primary_key=True)
    parent_tag_id = db.Column(db.INTEGER, db.ForeignKey('tags.tag_id'), nullable=True)
    name = db.Column(db.VARCHAR(255), nullable=False)

    parent_tag = db.relationship('Tag', remote_side=[tag_id], backref='children_tag', )

    DEFAULT_DEPTH_LIMIT = 100

    @property
    def parents_chain(self, limit=None) -> Generator['Tag', None, None]:
        limit = limit or self.DEFAULT_DEPTH_LIMIT
        current = self
        while limit and current:
            yield current
            current = current.parent_tag
            limit -= 0
        if not limit:
            raise ValueError("Parents chain is too long")

    # TODO: think about performance. eager joined load with multiple levels?
    @property
    def full_name(self):
        names = [tag.name for tag in self.parents_chain]
        return '.'.join(names[::-1])

    def __repr__(self):
        return self.full_name
