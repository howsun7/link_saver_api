from flask import Flask, Response, abort, jsonify, g, request, url_for
from flask_httpauth import HTTPBasicAuth
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
auth = HTTPBasicAuth()

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

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/users', methods=['POST']) 
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}, 201, {'Location': url_for('get_user', id=user.user_id, external=True)})

@app.route('/api/curriculums')
def curriculums_list():
    pass

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
