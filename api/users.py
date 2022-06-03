from flask import Blueprint, Response

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/curriculums')
def index():
	return Response('currciulums')

