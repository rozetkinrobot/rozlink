from flask import Flask, render_template, redirect, request, abort
# from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object("rozlink.config")
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
# sess = Session(app)
# sess.init_app(app)

from rozlink import models, routes, api  # noqa

db.create_all()
