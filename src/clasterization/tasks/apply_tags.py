import logging

import celery

from admin.app import app, db
from admin.models.articles import tag_to_article_text, Article
from admin.models.articles_es import ArticleTextEs
from admin.models.tag_rules_es import TagRuleEs


logger = logging.getLogger(__name__)


@celery.task(queue='clasterization')
def apply_tags_task(article_id):
    logger.info("Adding tags for %s: started...", article_id)
    with app.app_context():
        db_article: Article = Article.query.get(article_id)
        article = ArticleTextEs.get(article_id)
        search = TagRuleEs.search() \
            .query(
                'percolate',
                field='query',
                document=article.to_dict()
            )
        total_count = search.count()
        search = search[0:total_count]
        tag_list = search.execute()
        logger.info("Adding tags for %s: total count to insert - %s", article_id, total_count)
        for tag_rule in tag_list:
            insert_statement = tag_to_article_text.insert().values(
                text_id=db_article.last_text_id,
                article_id=article_id,
                rule_id=tag_rule.meta.id,
                tag_id=tag_rule.tag_id,
            ).prefix_with('IGNORE')
            logger.info("Adding tags for %s: added tag %s", article_id, tag_rule.tag_id)
            db.session.execute(insert_statement)
        db.session.commit()
        logger.info("Adding tags for %s: done", article_id)
