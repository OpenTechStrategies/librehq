from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://librehq@localhost/librehq_core';

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from librehq import main
from librehq import account

import wikis

app.register_blueprint(main.bp);
app.register_blueprint(wikis.bp);

if __name__ == "__librehq__":
    app.run(host='0.0.0.0')
