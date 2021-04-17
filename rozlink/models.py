from flask_login import UserMixin
from rozlink import app, db, login_manager
from rozlink.utils.views import int2ip
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.Integer)
    link_id = db.Column(db.Integer, db.ForeignKey("link.id"))
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def toJson(self):
        return {"id": self.id, "ip": int2ip(self.ip_address), "l_id": self.link_id, "time": self.time}


class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    large_link = db.Column(db.String(1024))
    short_link = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)
    views = db.relationship("View", backref="link", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def toJson(self):
        return {"id": self.id, "ll": self.large_link, "sl": app.config["SERVER_URI"] + "/" + self.short_link, "views": [view.toJson() for view in self.views], "user_id": self.user_id, "time": self.time, "is_active": self.is_active}


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    links = db.relationship("Link", backref="user", lazy="dynamic")
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
