from elasticsearch_dsl import Document, Text, Integer, Keyword


SUPPORTED_LANGUAGES_ANALYZER_MAPPING = {
    'uk': 'ukrainian',
    'en': 'english',
    'ru': 'russian',
}


class ArticleTextEs(Document):
    """
    Has the same meaning as sqlalchemy's ArticleText model, but also stores some Article data
    """
    article_id = Integer()
    site_id = Integer()
    language = Keyword(required=True)
    url = Keyword(required=True)

    title = Text(required=False, fields={
        lang: Text(analyzer=analyzer)
        for lang, analyzer in SUPPORTED_LANGUAGES_ANALYZER_MAPPING.items()
    })
    content = Text(required=False, fields={
        lang: Text(analyzer=analyzer)
        for lang, analyzer in SUPPORTED_LANGUAGES_ANALYZER_MAPPING.items()
    })

    class Index:
        name = 'article_texts'
        settings = {
          "number_of_shards": 2,
        }
