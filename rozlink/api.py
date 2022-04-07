from rozlink import app, db
from flask import request, jsonify
from flask_login import current_user
from rozlink.models import Link


def get_error(error, str_err=None):
    if app.config["DEBUG"] == "True":
        return {"success": False, "reason": error, "str_err": str(str_err)}
    else:
        return {"success": False, "reason": error}


def get_success(data):
    return {"success": True, "data": data}


@app.route('/api/v1/link_info', methods=["POST"])
def link_info():
    if current_user.is_authenticated:
        data = request.json
        try:
            link_id = data["id"]
            link = Link.query.filter_by(id=link_id).first()
            if link.user_id != current_user.id:
                return jsonify(get_error(403)), 403
            if link.is_deleted:
                return jsonify(get_error("Link deleted")), 403
            return get_success(link.toJson())
        except TypeError as e:
            return jsonify(get_error(400, e)), 400
        except AttributeError as e:
            return jsonify(get_error(400, e)), 400
        except KeyError as e:
            return jsonify(get_error(400, e)), 400
        except ValueError as e:
            return jsonify(get_error(400, e)), 400

    return jsonify(get_error(401)), 401


@app.route('/api/v1/set_link_state', methods=["POST"])
def set_link_state():
    if current_user.is_authenticated:
        data = request.json
        try:
            link_id = data["id"]
            state = bool(data["state"])
            link = Link.query.filter_by(id=link_id).first()
            if link.user_id != current_user.id:
                return jsonify(get_error(403)), 403
            if link.is_deleted:
                return jsonify(get_error("Link deleted")), 403
            link.is_active = state
            db.session.add(link)
            db.session.commit()
            return get_success({"is_active": int(link.is_active)})
        except TypeError:
            return jsonify(get_error(400)), 400
        except AttributeError:
            return jsonify(get_error(400)), 400
        except KeyError:
            return jsonify(get_error(400)), 400
        except ValueError:
            return jsonify(get_error(400)), 400

    return jsonify(get_error(401)), 401


@app.route('/api/v1/delete_link', methods=["POST"])
def delete_link():
    if current_user.is_authenticated:
        data = request.json
        try:
            link_id = data["id"]
            link = Link.query.filter_by(id=link_id).first()
            if link.user_id != current_user.id:
                return jsonify(get_error(403)), 403
            link.is_deleted = True
            link.is_active = False
            db.session.add(link)
            db.session.commit()
            return get_success(None)
        except TypeError:
            return jsonify(get_error(400)), 400
        except AttributeError:
            return jsonify(get_error(400)), 400
        except KeyError:
            return jsonify(get_error(400)), 400
        except ValueError:
            return jsonify(get_error(400)), 400

    return jsonify(get_error(401)), 401
