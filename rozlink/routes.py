from rozlink import app, db, login_manager
import netaddr
import os
from flask import request, redirect, abort, render_template, url_for, send_from_directory, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from rozlink.forms import LoginForm, RegisterForm, LinkForm
from rozlink.models import User, Link, View
from rozlink.utils.links import create_unique_link, is_safe_url
from rozlink.utils.views import ip2int


def redirect_dest(fallback):
    dest = request.args.get('next')
    if is_safe_url(dest):
        try:

            dest_url = url_for(dest)
        except:
            return redirect(fallback)
        return redirect(dest_url)
    return redirect(fallback)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LinkForm(request.form)

    if form.validate_on_submit():
        large_link = form.link.data
        if large_link:
            if "://" not in large_link:
                large_link = "https://" + large_link
            short_link = create_unique_link()

            dblink = Link(large_link=large_link, short_link=short_link)
            if current_user.is_authenticated:
                current_user.links.append(dblink)
                db.session.add(current_user)
            else:
                links = session.get("links", [])
                links.append(dblink.short_link)
                session["links"] = links
                db.session.add(dblink)
            db.session.commit()

            return render_template("index.html", form=form, reslink=dblink.short_link)
        return render_template("index.html", form=form, reslink=None, errors=["URL lenght must not be 0..."])
    return render_template('index.html', form=form, reslink=None, errors=None)


@app.route('/<short_link>')
def short_link_redir(short_link):
    dblink = Link.query.filter_by(
        short_link=short_link, is_active=True).first()
    if dblink:
        new_view = View(ip_address=ip2int(
            request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
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
            return render_template("register.html", form=form, errors=["User already exists"])
        new_user = User(login=form.login.data, email=form.email.data)
        new_user.set_password(form.password.data)
        links = session.get("links", [])
        for link in links:
            dblink = Link.query.filter_by(short_link=link).first()
            if dblink.user_id is None:
                new_user.links.append(dblink)
        session["links"] = []

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect_dest(fallback=url_for('index'))

    return render_template("register.html", form=form, errors=None)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        log_user = User.query.filter_by(login=form.login.data).first()
        if log_user:
            if log_user.check_password(form.password.data):
                links = session.get("links", [])
                for link in links:
                    dblink = Link.query.filter_by(short_link=link).first()
                    if dblink.user_id is None:
                        log_user.links.append(dblink)
                session["links"] = []
                db.session.add(log_user)
                db.session.commit()

                login_user(log_user, remember=form.remember_me.data)
                return redirect_dest(fallback=url_for('index'))
                # return redirect(next_url or url_for('index'))
        return render_template("login.html", form=form, errors=["Login and password doesn't match"])
    return render_template("login.html", form=form, errors=None)


@app.route('/profile')
@login_required
def profile():
    links = current_user.links.all()
    total_links = len(links)
    total_views = 0
    ips = []
    for link in links:
        total_views += len(link.views.all())
        for view in link.views.all():
            ips.append(view.ip_address)
    unique_ips = len(list(set(ips)))

    return render_template("profile.html", links=links, total_links=total_links, total_views=total_views, unique_ips=unique_ips)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img/'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@login_manager.unauthorized_handler
def handle_needs_login():
    # flash("You have to be logged in to access this page.")
    return redirect(url_for('login', next=request.endpoint))
