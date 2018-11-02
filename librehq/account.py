from flask import (
    Blueprint, render_template
)
from librehq import db

bp = Blueprint('account', __name__, url_prefix='/')

@bp.route('/signup', methods=(["POST", "GET"]))
def signup():
    return render_template("signup.html")

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
