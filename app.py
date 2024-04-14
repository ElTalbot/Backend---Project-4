from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_marshmallow import Marshmallow

from flask_bcrypt import Bcrypt

from config.environment import db_URI

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello():
    return "Hello, World!"

app.config["SQLALCHEMY_DATABASE_URI"] = db_URI

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

marsh = Marshmallow(app)

from controllers import sessions, users, movements, posts

app.register_blueprint(sessions.router, url_prefix="/api")

app.register_blueprint(users.router, url_prefix="/api")

app.register_blueprint(movements.router, url_prefix="/api")

app.register_blueprint(posts.router, url_prefix="/api")