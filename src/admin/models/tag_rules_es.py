from elasticsearch_dsl import Document, Integer, Percolator


class TagRuleEs(Document):
    tag_id = Integer()
    query = Percolator()

    class Index:
        name = 'tag_rules'
        settings = {
          "number_of_shards": 2,
        }
