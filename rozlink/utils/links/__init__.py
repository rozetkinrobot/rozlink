from secrets import token_hex
from rozlink.models import Link


def create_unique_link():
    i = 1
    while True:
        i += 1
        short_link = token_hex(i)
        if not Link.query.filter_by(short_link=short_link).first():
            break
    return short_link
