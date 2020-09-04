from admin.app import db


class RuleTypes:
    ES_QUERY = 'es_query'
    KEYWORD_LIST = 'keyword_list'
    MACHINE_LEARNING = 'machine_learning'

    ALL = [ES_QUERY, KEYWORD_LIST, MACHINE_LEARNING]


class TagRule(db.Model):
    __tablename__ = 'tag_rules'
    rule_id = db.Column(db.INTEGER, primary_key=True)
    tag_id = db.Column(db.INTEGER, nullable=False)
    rule_type = db.Column(db.Enum(*RuleTypes.ALL), nullable=False)
    rule_language = db.Column(db.VARCHAR(3), nullable=False)
    rule_query = db.Column(db.TEXT, nullable=False)
    creator_id = db.Column(db.INTEGER, nullable=False)
    enabled_timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    disabled_timestamp = db.Column(db.TIMESTAMP, nullable=True)
