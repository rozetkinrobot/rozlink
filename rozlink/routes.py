from rozlink import app, db, login_manager
import os
from flask import request, redirect, abort, render_template, url_for, send_from_directory, session
from flask_login import login_user, login_required, logout_user, current_user
from rozlink.forms import LoginForm, RegisterForm, LinkForm, ChangePassForm
from rozlink.models import User, Link, View
from rozlink.utils.links import create_unique_link, is_safe_url
from rozlink.utils.views import ip2int, int2ip

if app.config["HAS_TELEGRAM_BOT"]:
    from rozlink.telegram_bot import send_view

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
        return render_template("index.html", form=form, reslink=None, errors=["URL length must not be 0..."])
    return render_template('index.html', form=form, reslink=None, errors=form.error_list)


@app.route('/<short_link>')
def short_link_redir(short_link):
    dblink = Link.query.filter_by(
        short_link=short_link, is_active=True, is_deleted=False).first()
    if dblink:
        new_view = View(ip_address=ip2int(
            request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
        dblink.views.append(new_view)
        db.session.add(dblink)
        db.session.commit()

        db_user = User.query.filter_by(id=dblink.user_id).first()
        if app.config["HAS_TELEGRAM_BOT"]:
            if db_user:
                if db_user.telegram_id:
                    send_view(db_user.telegram_id, dblink.short_link, int2ip(
                        new_view.ip_address), views_count=dblink.views.count())

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

    return render_template("register.html", form=form, errors=form.error_list)


@app.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePassForm(request.form)
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            return render_template("change_password.html", form=form, errors=["Old password is wrong"])

        current_user.set_password(form.password.data)

        db.session.add(current_user)
        db.session.commit()

        return redirect_dest(fallback=url_for('index'))
    return render_template("change_password.html", form=form, errors=form.error_list)


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
        return render_template("login.html", form=form, errors=["Login and password doesn't match"])
    return render_template("login.html", form=form, errors=form.error_list)


@app.route('/profile')
@login_required
def profile():
    links = current_user.links.filter_by(is_deleted=False).all()
    total_links = len(links)
    total_views = 0
    ips = []
    if current_user.is_admin:
        admin_total_links = Link.query.count()
        admin_total_views = View.query.count()
        admin_total_users = User.query.count()
    else:
        admin_total_links = 0
        admin_total_views = 0
        admin_total_users = 0
    for link in links:
        total_views += len(link.views.all())
        for view in link.views.all():
            ips.append(view.ip_address)
    unique_ips = len(list(set(ips)))

    return render_template("profile.html", links=links, total_links=total_links, total_views=total_views, unique_ips=unique_ips, admin_total_links=admin_total_links, admin_total_views=admin_total_views, admin_total_users=admin_total_users)


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
    return redirect(url_for('login', next=request.endpoint))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
