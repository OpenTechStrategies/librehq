from flask import (
    Blueprint, render_template, request
)
from flask_mail import Message
from librehq import db, mail

bp = Blueprint('account', __name__, url_prefix='/')

@bp.route('/signup', methods=(["POST", "GET"]))
def signup():
    if request.method == "POST":
        msg = Message("Validate",
                      sender="bot@librehq.com",
                      recipients=[request.form["email"]])
        msg.body = "Please validate:"
        mail.send(msg)
        return "See email for validation link"
    else:
        return render_template("signup.html")

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
