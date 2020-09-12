from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse, ParseResult
from werkzeug.datastructures import MultiDict


def update_get_args(url, **params):
    url_parsed = urlparse(url)
    query_dict = MultiDict(parse_qsl(url_parsed.query))
    query_dict.update(params)

    url_parsed = ParseResult(
        scheme=url_parsed.scheme,
        netloc=url_parsed.netloc,
        path=url_parsed.path,
        params=url_parsed.params,
        query=urlencode(tuple(query_dict.items(multi=True))),
        fragment=url_parsed.params
    )
    return urlunparse(url_parsed)
