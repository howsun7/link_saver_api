from flask import Flask, Response, abort, jsonify, g, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .errors import errors
from .models import db, migrate, User
from .users import users


def create_app(config):
    app = Flask(__name__)
    # db = SQLAlchemy(app)
    # migrate = Migrate(app, db)
    auth = HTTPBasicAuth()
    app.config.from_object(config)
    
    register_extensions(app)
    return app

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(errors)
    app.register_blueprint(users)
    
app = create_app('config.Config')

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


@app.route('/api/curriculums')
def get_curriculums():
    pass

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


