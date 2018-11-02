from flask import (
    Blueprint, render_template
)

import wikis
from librehq import account

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('')
def index():
    return account.signup()

@bp.route('/dashboard')
def dashboard():
    modules = [
        wikis.main_partial()
    ]
    return render_template("index.html", modules=modules)
