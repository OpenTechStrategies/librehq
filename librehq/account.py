from flask import (
    Blueprint, render_template, request, url_for
)
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from librehq import db, mail, app
import random

bp = Blueprint('account', __name__, url_prefix='/')

def signin():
    return render_template("signin.html")

@bp.route('/signup', methods=(["POST"]))
def signup():
    new_account = Account(username=request.form["username"],
                          #TODO: Stored as plain text!  Change before launch!
                          #See model definition as to logic
                          password=request.form["password"],
                          email=request.form["email"])
    db.session.add(new_account)
    db.session.commit()

    msg = Message("Validate",
                  sender="bot@librehq.com",
                  recipients=[request.form["email"]])
    msg.body = ("Please validate: " +
            url_for("account.activate", token=generate_token(new_account), _external=True))
    mail.send(msg)
    return "See email for validation link"

@bp.route('/activate')
def activate():
    email = confirm_token(request.args.get('token'), 3600)
    if email:
        account = Account.query.filter_by(email=email).first_or_404()
        account.validated = True
        db.session.add(account)
        db.session.commit()
        return "Confirmed!"
    else:
        return "Unable to confirm!"

def generate_token(account):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(account.email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))

    # Right now, this is being stored as plain text!
    # TODO: Hash this correctly
    #
    # Because this password is going to be used in subservices
    # for authentication until we have correct authentication set up,
    # we either need to query the user each time they want to do
    # something that would pass through their password, or store it
    # as plain text so we can reuse.  We choose the second so that
    # while prototyping, the user experience matches the end goal.
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    validated = db.Column(db.Boolean, default=False)
