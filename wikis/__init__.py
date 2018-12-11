from flask import (
    redirect, session
)

db = None

def signin_required(view):
    def wrapped_view(**kwargs):
        if session.get("account_username") is None:
            return redirect("/")
        else:
            return view(**kwargs)
    wrapped_view.__name__ = view.__name__

    return wrapped_view

def initialize_module(app, app_db):
    global db
    db = app_db

    from wikis import wiki
    app.register_blueprint(wiki.bp)
