from flask import Blueprint, Response

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(400)
def unfound_error(error):
    return Response(f'Not found. Error: {error}', status=400)

@errors.app_errorhandler(Exception)
def server_error(error):
    return Response(f"Oops, got an error! {error}", status=500)
