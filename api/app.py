from flask import Flask, Response, abort, jsonify, g, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .errors import errors
from .models import db, migrate, User
from .users import users


def create_app(config):
    app = Flask(__name__)    
    app.config.from_object(config)
    
    register_extensions(app)
    return app

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(errors)
    app.register_blueprint(users)


app = create_app('config.Config')
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@app.route("/")
@auth.login_required
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



