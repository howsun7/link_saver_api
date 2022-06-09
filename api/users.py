from flask import Blueprint, Response, request, abort, jsonify, url_for, g

from .auth import auth
from .models import User, db, Curriculum, Topic


users = Blueprint('users', __name__, url_prefix='/api/users')


@users.route('/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
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
    return jsonify({'username': user.username}, 201, {'Location': url_for('users.get_user', user_id=user.id, _external=True)})

@users.route('/<int:user_id>/curriculums')
def get_user_curriculums(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(400)        
    curriculums = user.curriculums.all()
    return jsonify({'curriculums': curriculums})

@users.route('/<int:user_id>/curriculums', methods=['POST'])
def create_user_curriculum(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(400)
    curriculum_name = request.json.get('curriculumName')
    curriculum = Curriculum(name=curriculum_name)
    user.curriculums.append(curriculum)
    db.session.add(user)
    db.session.add(curriculum)
    db.session.commit()
    return jsonify({'curriculum': curriculum.name}, 201, {'Location': url_for('users.get_user_curriculums', user_id=user.id, _external=True)})

