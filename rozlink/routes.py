from rozlink import app, db
import netaddr
import os
from flask import request, redirect, abort, render_template, url_for, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from rozlink.forms import LoginForm, RegisterForm, LinkForm
from rozlink.models import User, Link, View
from rozlink.utils.links import create_unique_link
from rozlink.utils.views import ip2int


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LinkForm(request.form)

    if form.validate_on_submit():
        large_link = form.link.data
        if  "://" not in large_link:
            large_link = "http://" + large_link
        if large_link:
            dblink = Link.query.filter_by(large_link=large_link).first()
            if not dblink:
                short_link = create_unique_link()
                dblink = Link(large_link=large_link, short_link=short_link)
                db.session.add(dblink)
                db.session.commit()
            print("success")
            return render_template("index.html", form=form, reslink=dblink.short_link)
    return render_template('index.html', form=form, reslink=None, errors=None)


@app.route('/<short_link>')
def short_link_redir(short_link):
    dblink = Link.query.filter_by(short_link=short_link).first()
    if dblink:
        new_view = View(ip_address=ip2int(request.remote_addr))
        dblink.views.append(new_view)
        db.session.add(dblink)
        db.session.commit()
        return redirect(dblink.large_link)
    abort(404)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        reg_user = User.query.filter_by(login=form.login.data).first()
        reg_user1 = User.query.filter_by(email=form.email.data).first()
        if reg_user or reg_user1:
            return render_template("register_alt.html", form=form, errors=["User already exists"])
        new_user = User(login=form.login.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("index"))

    return render_template("register.html", form=form, errors=None)

    pass


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        log_user = User.query.filter_by(login=form.login.data).first()
        if log_user:
            if log_user.check_password(form.password.data):
                login_user(log_user, remember=form.remember_me.data)
                return redirect(url_for("index"))
        return render_template("login.html", form=form, errors=["Login or password doesn't match"])
    # if request.args.get("alt"):
    #     return render_template("login_alt.html", form=form, errors=[None])
    return render_template("login.html", form=form, errors=None)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img/'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
