from rozlink import app, db
import netaddr
from flask import request, redirect, abort, render_template, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from rozlink.forms import LoginForm, RegisterForm, LinkForm
from rozlink.models import User, Link, View
from rozlink.utils.links import create_unique_link
from rozlink.utils.views import ip2int
import json


def get_error(error):
    return {"success": False, "reason": error}


def get_success(data):
    return {"success": True, "data": data}


@app.route('/api/v1/link_info')
def link_info():
    if current_user.is_authenticated:
        data = request.form.get("payload")
        try:
            js_data = json.loads(data)
            link_id = js_data["id"]
            link = Link.query.filter_by(id=link_id).first()
            if link.user_id != current_user.id:
                return jsonify(get_error(403))
            return get_success(link.toJson())
        except TypeError:
            return jsonify(get_error(400))
        except KeyError:
            return jsonify(get_error(400))
        except ValueError:
            return jsonify(get_error(400))

    return jsonify(get_error(401))
