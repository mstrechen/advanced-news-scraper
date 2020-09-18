from elasticsearch_dsl import Document, Integer, Percolator, Text

from admin.models.articles_es import SUPPORTED_LANGUAGES_ANALYZER_MAPPING


class TagRuleEs(Document):
    tag_id = Integer()
    query = Percolator()

    title = Text(required=False, fields={
        lang: Text(analyzer=analyzer)
        for lang, analyzer in SUPPORTED_LANGUAGES_ANALYZER_MAPPING.items()
    })
    content = Text(required=False, fields={
        lang: Text(analyzer=analyzer)
        for lang, analyzer in SUPPORTED_LANGUAGES_ANALYZER_MAPPING.items()
    })

    class Index:
        name = 'tag_rules'
        settings = {
          "number_of_shards": 2,
        }
