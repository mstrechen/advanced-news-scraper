import logging

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from admin.models.articles import Article as ArticleModel, ArticleText as ArticleTextModel

from admin.models.sites import Site as SiteModel
from admin.models.tags import Tag as TagModel


class Site(SQLAlchemyObjectType):
    base_url = graphene.String()

    class Meta:
        model = SiteModel
        interfaces = (relay.Node, )


class Tag(SQLAlchemyObjectType):
    name = graphene.String()
    full_name = graphene.String()

    class Meta:
        model = TagModel
        interfaces = (relay.Node, )


class ArticleText(SQLAlchemyObjectType):
    title = graphene.String()
    content = graphene.String()

    class Meta:
        model = ArticleTextModel
        interfaces = (relay.Node,)


class Article(SQLAlchemyObjectType):
    tags = graphene.List(Tag)
    text = ArticleText

    class Meta:
        model = ArticleModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_articles = SQLAlchemyConnectionField(Article.connection)
    all_sites = SQLAlchemyConnectionField(Site.connection)
    all_tags = SQLAlchemyConnectionField(Tag.connection)

    article_by_id = graphene.Field(Article, article_id=graphene.String(required=True))

    def resolve_article_by_id(parent, info, article_id):
        logger = logging.getLogger(__name__)
        logger.warning("Some log", extra=dict(some="extra"))
        return ArticleModel.query.get(article_id)


schema = graphene.Schema(query=Query)
