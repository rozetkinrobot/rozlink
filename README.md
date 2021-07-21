# rozlink
<img src="https://github.com/rozetkinrobot/rozlink/blob/a5f6ffafd18c9491325cc7d26a342ffef8fdc875/rozlink/static/img/rozlink_logo1.png?raw=true"  width="814" height="160"></img>

This is a simple link shortifier flask site writed with bulma

[Example site](https://rozlink.ru)
## Features
* Google Recaptcha support
* Accounts
* Link statistics
* QR Code generating

## Usage
1. Install requirements
```shell
python3 -m pip intstall -r requirements.txt
```

2. **IMPORTANT** Replace configuration values in rozlink/config.py
```python
SECRET_KEY = 'YOUR_SECRET_KEY'
RECAPTCHA_PUBLIC_KEY = 'YOUR_RECAPTCHA_PUBLIC_KEY'
RECAPTCHA_PRIVATE_KEY = 'YOUR_RECAPTCHA_SECRET_KEY'
```

3. Launch app with Flask
```shell
export FLASK_APP=wsgi.app
python3 -m flask run
```

