from sqlalchemy import event

from admin.app import db
from admin.models.tag_rules_es import TagRuleEs
from clasterization.query_translator import QueryTranslator

class RuleTypes:
    ES_QUERY = 'es_query'
    KEYWORD_LIST = 'keyword_list'
    MACHINE_LEARNING = 'machine_learning'

    ALL = [ES_QUERY, KEYWORD_LIST, MACHINE_LEARNING]


class TagRule(db.Model):
    __tablename__ = 'tag_rules'
    rule_id = db.Column(db.INTEGER, primary_key=True)
    tag_id = db.Column(db.INTEGER, db.ForeignKey('tags.tag_id'), nullable=False)
    rule_type = db.Column(db.Enum(*RuleTypes.ALL), nullable=False)
    rule_language = db.Column(db.VARCHAR(3), nullable=False)
    rule_query = db.Column(db.TEXT, nullable=False)
    creator_id = db.Column(db.INTEGER, db.ForeignKey('users.id'), nullable=False)
    enabled_timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    disabled_timestamp = db.Column(db.TIMESTAMP, nullable=True)

    tag = db.relationship('Tag', remote_side=[tag_id], backref='rules', )
    creator = db.relationship('User', remote_side=[creator_id])


@event.listens_for(TagRule, 'after_insert')
@event.listens_for(TagRule, 'after_update')
def article_on_create_or_update(mapper, connection, tag_rule: TagRule):
    es_entity = TagRuleEs(
        meta={'id': tag_rule.rule_id},
        tag_id=tag_rule.tag_id,
        query=QueryTranslator(tag_rule.rule_query).translate()
    )
    es_entity.save()
