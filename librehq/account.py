from flask import (
    Blueprint, flash, render_template, redirect, request, session, url_for,
    jsonify
)
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from librehq import db, mail, app
import random

bp = Blueprint('account', __name__, url_prefix='/')

def signin():
    return render_template("signin.html")

def sendValidationEmail(account):
    msg = Message("Validate",
                  sender="bot@librehq.com",
                  recipients=[request.form["email"]])
    msg.body = ("Please validate: " +
            url_for("account.activate", token=generate_token(account), _external=True))
    mail.send(msg)

@bp.route('/signup', methods=(["POST"]))
def signup():
    new_account = Account(username=request.form["username"],
                          #TODO: Stored as plain text!  Change before launch!
                          #See model definition as to logic
                          password=request.form["password"],
                          email=request.form["email"])
    db.session.add(new_account)
    db.session.commit()

    sendValidationEmail(new_account)

    return "See email for validation link"

@bp.route('/signin', methods=(["POST"]))
def signin():
    username = request.form["username"]
    password = request.form["password"]

    account = Account.query.filter_by(username=username,
        password=password,
        validated=True).first()
    if account is not None:
        session['account_id'] = account.id
        session['account_username'] = account.username
        session['account_password'] = account.password
    resp = redirect("/")
    resp.set_cookie(
            key = 'librehq_user',
            value = session.get('account_username'),
            domain = request.headers['Host'])
    return resp

@bp.route('/signout')
def signout():
    session.clear()
    resp = redirect("/")
    resp.set_cookie(
            key = 'librehq_user',
            expires = 0,
            domain = request.headers['Host'])
    return resp

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

def signin_required(view):
    def wrapped_view(**kwargs):
        if session.get("account_id") is None:
            return redirect("/")
        else:
            return view(**kwargs)

    wrapped_view.__name__ = view.__name__

    return wrapped_view

@bp.route('/account')
@signin_required
def account():
    return render_template("account.html")

@bp.route("/account-data", methods=(["GET"]))
@signin_required
def account_data():
    account = Account.query.get(session.get("account_id"))
    return jsonify({
        "account": {
            "username": account.username,
            "email": account.email
        }
    })

@bp.route("/updateAccount", methods=(["POST"]))
@signin_required
def updateAccount():
    account = Account.query.get(session.get("account_id"))

    if not request.form["current_password"] == account.password:
        flash("Current password doesn't match")
        return redirect(url_for(".account"))

    if request.form["password"]:
        account.password = request.form["password"]

    if not account.email == request.form["email"]:
        emailUpdated = True
        account.email = request.form["email"]
        account.validated = False

    if not account.username == request.form["username"]:
        flash("Changing username isn't supported at this time")

    db.session.add(account)
    db.session.commit()

    if not account.validated:
        sendValidationEmail(account)
        signout()
        return "See email for validation link"
    else:
        return redirect(url_for(".account"))

@bp.route("/deleteAccount", methods=(["POST"]))
@signin_required
def deleteAccount():
    account = Account.query.get(session.get("account_id"))
    if not request.form["current_password"] == account.password:
        flash("Current password doesn't match")
        return redirect(url_for(".account"))

    flash("Deleting account isn't supported at this time")
    return redirect(url_for(".account"))

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
