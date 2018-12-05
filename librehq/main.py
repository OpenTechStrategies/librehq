from flask import (
    Blueprint, redirect, render_template, session
)

import wikis
from librehq import account

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('')
def index():
    if session.get("account_id") is None:
        return render_template("signin.html", signed_out=True)
    else:
        return redirect("/dashboard")

@bp.route('/dashboard')
@account.signin_required
def dashboard():
    modules = [
        wikis.main_partial()
    ]
    return render_template("dashboard.html", modules=modules)
