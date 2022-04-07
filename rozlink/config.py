SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 1800
SECRET_KEY = 'super_secret_key_f0r3v3r'
SESSION_TYPE = 'sqlalchemy'
SERVER_URI = 'http://rozlink.ru'
TESTING = False
RECAPTCHA_DATA_ATTRS = {'bind': 'submit-button',
                        'callback': 'onSubmitCallback', 'size': 'invisible'}
RECAPTCHA_PUBLIC_KEY = 'YOUR_RECAPTCHA_PUBLIC_KEY'
RECAPTCHA_PRIVATE_KEY = 'YOUR_RECAPTCHA_PRIVATE_KEY'

# TG BOT SECTION
HAS_TELEGRAM_BOT = True

TELEGRAM_BOT_NAME = 'rozlink_bot'
TELEGRAM_TOKEN = 'TELEGRAM_BOT_TOKEN'
WEBHOOK_URL_PATH = '/tg/webhook'

# Needed only for debug mode
WEBHOOK_SSL_CERT = './crt.pem'
WEBHOOK_SSL_PRIV = './key.pem'
