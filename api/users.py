from flask import Blueprint, Response, request, abort, jsonify, url_for, g


from .models import User, db

users = Blueprint('users', __name__, url_prefix='/api/users')


@users.route('/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@users.route('', methods=['POST']) 
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
    return jsonify({'username': user.username}, 201, {'Location': url_for('get_user', id=user.user_id, _external=True)})


@users.route('/<int:user_id>/curriculums')
def index(user_id):
	return Response('currciulums')

