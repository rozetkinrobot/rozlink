SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'super_secret_key_f0r3v3r'
SESSION_TYPE = 'sqlalchemy'
SERVER_URI = 'http://rozlink.ru'
TESTING = False
RECAPTCHA_DATA_ATTRS = {'bind': 'submit-button',
                        'callback': 'onSubmitCallback', 'size': 'invisible'}
RECAPTCHA_PUBLIC_KEY = 'YOUR_RECAPTCHA_PUBLIC_KEY'
RECAPTCHA_PRIVATE_KEY = 'YOUR_RECAPTCHA_SECRET_KEY'
