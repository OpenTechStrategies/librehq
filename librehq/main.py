from flask import (
    Blueprint, redirect, render_template, session, get_flashed_messages,
    jsonify
)

from librehq import account

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route("/getmessages")
def get_messages():
    return jsonify(get_flashed_messages())

@bp.route('')
def index():
    if session.get("account_id") is None:
        return render_template("signin.html", signed_out=True)
    else:
        return redirect("/dashboard")

@bp.route('/dashboard')
@account.signin_required
def dashboard():
    return render_template("dashboard.html")
