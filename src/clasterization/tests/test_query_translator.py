# flake8: noqa

import json

import pytest

from clasterization.query_translator import QueryDecodeError, QueryTranslator


@pytest.mark.parametrize(
    'query, expected',
    [
        (
            '"Сказали що світ"',
            {"multi_match": {"type": "phrase", "query": "Сказали що світ", "fields": ["title", "content"]}}
        ),
        (
            '{"lang": "uk", "keywords": ["Колись", "Мені"]}',
            {
                "bool": {
                    "should": [
                        {"multi_match": {"type": "phrase", "query": "Колись", "fields": ["title.uk", "content.uk"]}},
                        {"multi_match": {"type": "phrase", "query": "Мені", "fields": ["title.uk", "content.uk"]}}
                    ],
                    "minimum_should_match": 1
                }
            }
        ),
        (
            '["Сказали", "світ"]',
            {
                "bool": {
                    "should": [
                        {"multi_match": {"type": "phrase", "query": "Сказали", "fields": ["title", "content"]}},
                        {"multi_match": {"type": "phrase", "query": "світ", "fields": ["title", "content"]}}
                    ]
                }
            }
        ),
        (
            '{"synonyms": '
            '[{"min_count": 2, "keywords": ["one", "two", "three"]},'
            ' {"synonyms": [{"min_count": -1, "keywords": ["do", "you", "love", "me"]}],'
            '  "antonyms": ["still"]'
            ' }'
            ']}',
            {
                "bool": {
                    "should": [
                        {
                            "bool": {
                                "should": [
                                    {"multi_match": {"type": "phrase", "query": "one", "fields": ["title", "content"]}},
                                    {"multi_match": {"type": "phrase", "query": "two", "fields": ["title", "content"]}},
                                    {"multi_match": {"type": "phrase", "query": "three", "fields": ["title", "content"]}}
                                ],
                                "minimum_should_match": 2
                            }
                        },
                        {
                            "bool": {
                                "should": [
                                    {
                                        "bool": {
                                            "should": [
                                                {"multi_match": {"type": "phrase", "query": "do", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "you", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "love", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "me", "fields": ["title", "content"]}}
                                            ],
                                            "minimum_should_match": 4
                                        }
                                    }
                                ],
                                "must_not": [
                                    {
                                        "bool": {
                                            "should": [
                                                {"multi_match": {"type": "phrase", "query": "do", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "you", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "love", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "me", "fields": ["title", "content"]}}
                                            ],
                                            "minimum_should_match": 4
                                        }
                                    }
                                ]
                            }
                        }
                    ],
                    "must_not": [
                        {
                            "bool": {
                                "should": [
                                    {"multi_match": {"type": "phrase", "query": "one", "fields": ["title", "content"]}},
                                    {"multi_match": {"type": "phrase", "query": "two", "fields": ["title", "content"]}},
                                    {"multi_match": {"type": "phrase", "query": "three", "fields": ["title", "content"]}}
                                ],
                                "minimum_should_match": 2
                            }
                        },
                        {
                            "bool": {
                                "should": [
                                    {
                                        "bool": {
                                            "should": [
                                                {"multi_match": {"type": "phrase", "query": "do", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "you", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "love", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "me", "fields": ["title", "content"]}}
                                            ],
                                            "minimum_should_match": 4
                                        }
                                    }
                                ],
                                "must_not": [
                                    {
                                        "bool": {
                                            "should": [
                                                {"multi_match": {"type": "phrase", "query": "do", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "you", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "love", "fields": ["title", "content"]}},
                                                {"multi_match": {"type": "phrase", "query": "me", "fields": ["title", "content"]}}
                                            ],
                                            "minimum_should_match": 4
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        )
    ]
)
def test_positive(query, expected):
    print(json.dumps(QueryTranslator(query).translate().to_dict(), ensure_ascii=False), flush=True)
    assert QueryTranslator(query).translate().to_dict() == expected


@pytest.mark.parametrize(
    'query',
    [
        '{broken json',
        '{}',
        '[]',
        '{"keywords": []}',
        '{"keywords": [{}]}',
    ]
)
def test_negative(query):
    with pytest.raises(QueryDecodeError):
        QueryTranslator(query).translate()
