from flask import Flask, Response, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .errors import errors
from .users import users



app = Flask(__name__)
app.register_blueprint(errors)
app.register_blueprint(users)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import User

@app.route("/")
def index():
    return Response("Hello, world!", status=200)


@app.route("/custom", methods=["POST"])
def custom():
    payload = request.get_json()

    if payload.get("say_hello") is True:
        output = jsonify({"message": "Hello!"})
    else:
        output = jsonify({"message": "..."})

    return output


@app.route("/health")
def health():
    return Response("OK", status=200)
