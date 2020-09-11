import json
from typing import Union, List

import elasticsearch_dsl.query as Q
from werkzeug.utils import cached_property


class QueryDecodeError(Exception):
    pass


class QueryTranslator:
    FIELDS = ['title', 'content']
    ALLOWED_TYPES = [str, list, dict]

    def __init__(self, query: str):
        self.query = self._decode_query(query)
        self.lang = self._extract_lang()

    def translate(self) -> Q.Query:
        return self._translate(self.query)

    def _translate(self, query) -> Q.Query:
        if type(query) not in self.ALLOWED_TYPES:
            raise QueryDecodeError('Invalid node type', repr(type(query)), repr(query))

        if type(query) is str:
            return Q.MultiMatch(type='phrase', query=query, fields=self.search_fields)
        if type(query) is list:
            if not query:
                raise QueryDecodeError("List should not be empty")
            return Q.Bool(should=[self._translate(subquery) for subquery in query])
        if type(query) is dict:
            return self._translate_dict_query(query)

    def _translate_dict_query(self, query: dict) -> Q.Query:
        if 'keywords' in query:
            keywords = query['keywords']
            min_cnt = query.get('min_count', 1)
            min_cnt = min_cnt if min_cnt != -1 else len(query['keywords'])
            if type(keywords) is not list:
                raise QueryDecodeError('"keywords" field should be a list, got ', repr(type(keywords)))
            if type(min_cnt) is not int:
                raise QueryDecodeError('"min_count" field should be an int, got ', repr(type(min_cnt)))
            if not keywords or len(keywords) < min_cnt:
                raise QueryDecodeError('"keywords" should be non-empty list with length not less than min_count')
            return Q.Bool(should=[self._translate(subquery) for subquery in keywords], minimum_should_match=min_cnt)
        if 'synonyms' not in query and 'antonyms' not in query:
            raise QueryDecodeError(
                'Dict subquery should have either keywords, antonyms or synonyms field, got',
                repr(query.keys())
            )
        synonyms = query.get('synonyms', [])
        antonyms = query.get('antonyms', [])
        if not synonyms and not antonyms:
            raise QueryDecodeError('Either "synonyms" or "antonyms" should be a non-empty list')
        if type(synonyms) is not list:
            raise QueryDecodeError('"synonyms" should have type list, got', repr(type(synonyms)))
        if type(antonyms) is not list:
            raise QueryDecodeError('"antonyms" should have type list, got', repr(type(antonyms)))
        return Q.Bool(
            should=[self._translate(subquery) for subquery in synonyms],
            must_not=[self._translate(subquery) for subquery in synonyms],
        )

    @cached_property
    def search_fields(self) -> List[str]:
        if not self.lang:
            return self.FIELDS
        return [f'{field}.{self.lang}' for field in self.FIELDS]

    @staticmethod
    def _decode_query(query: str) -> Union[dict, list, str]:
        try:
            return json.loads(query)
        except json.JSONDecodeError as e:
            raise QueryDecodeError(*e.args) from e

    def _extract_lang(self):
        if type(self.query) is not dict:
            return None
        return self.query.get('lang')
