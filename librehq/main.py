from flask import (
    Blueprint, render_template
)

import wikis

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('')
def index():
    modules = [
        wikis.main_partial()
    ]
    return render_template("index.html", modules=modules)
