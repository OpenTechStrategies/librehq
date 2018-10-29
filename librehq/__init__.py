from flask import Flask

app = Flask(__name__)

from librehq import main
import wikis

app.register_blueprint(main.bp);
app.register_blueprint(wikis.bp);

if __name__ == "__librehq__":
    app.run(host='0.0.0.0')
