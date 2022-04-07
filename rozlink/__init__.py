from flask import Flask, render_template, redirect, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object("rozlink.config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from rozlink import models, routes, api # noqa

db.create_all()

if app.config["HAS_TELEGRAM_BOT"]:
    from rozlink import bot_routes #noqa
    from rozlink.telegram_bot import bot
    bot.remove_webhook()
    url = app.config["SERVER_URI"] + app.config["WEBHOOK_URL_PATH"]
    bot.set_webhook(url=url)