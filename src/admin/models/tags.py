from admin.app import db


class Tag(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.INTEGER, primary_key=True)
    parent_tag_id = db.Column(db.INTEGER, db.ForeignKey('tags.tag_id'), nullable=True)
    name = db.Column(db.VARCHAR(255), nullable=False)

    parent_tag = db.relationship('Tag', remote_side=[tag_id], backref='children_tag', )

    def __repr__(self):
        return f'{self.tag_id} - {self.name}'
