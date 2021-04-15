from rozlink import app
from urllib.parse import urlparse, urljoin
from secrets import token_hex
from flask import request
from rozlink.models import Link


def create_unique_link():
    i = 1
    while True:
        i += 1
        short_link = token_hex(i)
        if not Link.query.filter_by(short_link=short_link).first():
            break
    return short_link


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
