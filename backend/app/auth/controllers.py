'''
  holds the blueprint routes for auth
'''
from flask import Blueprint,request, jsonify, make_response
from .models import User
from .utils import AuthError

# auth bp
auth_bp = Blueprint('auth', __name__)

@auth_bp.after_request
def after(response):
  # add to headers after controllers
  response.headers.add('Access-Control-Allow-Headers',
                       'Content-Type,Authorization,true')
  response.headers.add('Access-Control-Allow-Methods',
                       'GET,PATCH,POST,DELETE,OPTIONS')
  return response

@auth_bp.route('/test')
def test():
  # test
  return jsonify({'message': 'test'})


@auth_bp.errorhandler(AuthError)
def handle_auth_error(exception: AuthError):
  response = jsonify({
    'success': False,
    'code': exception.error['code'],
    'error': exception.error['error'],
    'message': exception.error['description']
  })
  response.status_code = exception.error['code']
  return response