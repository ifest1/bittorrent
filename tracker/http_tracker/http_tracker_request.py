from urllib.parse import urlparse
from urllib.parse import parse_qsl
from urllib.parse import urlencode
from urllib.parse import urlunparse

def http_tracker_request_url(tracker_url, **kwargs):
    url = urlparse(tracker_url)
    query =  url.query

    url_dict = dict(parse_qsl(query))
    url_dict.update(kwargs)

    url = urlunparse(url._replace(query=urlencode(url_dict)))

    return url
