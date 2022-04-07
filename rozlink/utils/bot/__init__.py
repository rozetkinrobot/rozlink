from secrets import token_hex
from rozlink.models import User

def create_unique_token():
    i = 8
    while True:
        i += 1
        token = token_hex(i)
        if not User.query.filter_by(telegram_token=token).first():
            break
        if i > 16:
            i = 8
    return token