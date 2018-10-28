from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

from librehq import main
import wikis

app.register_blueprint(main.bp);
app.register_blueprint(wikis.bp);
