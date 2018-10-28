from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('')
def index():
    return 'This is a stub'
