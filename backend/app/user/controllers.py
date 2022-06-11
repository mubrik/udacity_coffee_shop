'''
  holds the blueprint routes for users
'''
from typing import List
from flask import Blueprint, jsonify, request, abort
from .models import User
from ..auth import AuthError, auth_management as auth_m, requires_authentication, requires_authorization

# user bp
user_bp = Blueprint('user', __name__)

@user_bp.route('users/test')
def test():
  # test
  return jsonify({'message': 'test'})


@user_bp.route('/baristas/edit', methods=['POST', 'DELETE'])
@requires_authorization(['post:baristas', 'post:managers'])
def manage_barista(permission: str|List[str]):
  data = request.get_json()
  user_id = data['user_id']
  roles = ['rol_PRrubjxSFgct2EQ2'] # barista role id
  
  if not user_id:
    abort(422, 'user_id required')

  if request.method == 'POST':
    # add role
    try:
      # i feel i should be using async here?
      # not sure how that works in python for now
      auth_m.users.add_roles(user_id, roles)
      return jsonify({
        'success': True,
        'message': 'User added to barista role'
      }), 201
    except:
      abort(500, 'error adding roles')
  elif request.method == 'DELETE':
    # remove role
    try:
      auth_m.users.remove_roles(user_id, roles)
      return jsonify({
        'success': True,
        'message': 'Barista role has been removed'
      }), 201
    except:
      abort(500, 'error removing role')
  # not any method
  abort(405, 'method not allowed')

  
@user_bp.route('/managers/edit', methods=['POST', 'DELETE'])
@requires_authorization('post:managers')
def manage_manager(permission: str|List[str]):
  data = request.get_json()
  user_id = data['user_id']
  roles = ['rol_VTeR8Pn9PCmMVWqI'] # manager role id
  
  if not user_id:
    abort(422, 'user_id required')

  if request.method == 'POST':
    # add role
    try:
      auth_m.users.add_roles(user_id, roles)
      return jsonify({
        'success': True,
        'message': 'User added to manager role'
      }), 201
    except:
      abort(500, 'error adding role')
  elif request.method == 'DELETE':
    # remove role
    try:
      auth_m.users.remove_roles(user_id, roles)
      return jsonify({
        'success': True,
        'message': 'Manager role has been removed'
      }), 201
    except:
      abort(500, 'error removing role')
  # not any method
  abort(405, 'method not allowed')


@user_bp.route('/baristas/<barista_id>', methods=['PATCH'])
@requires_authorization(['update:baristas', 'update:managers'])
def update_barista(permissions, barista_id):
  print(permissions, barista_id)
  # get data
  request_data = request.get_json()
  user_id = request_data['user_id']
  new_username = request_data['username']
  # checks
  if new_username is None or user_id is None:
    abort(400, description='Error in body data')
    
  # verify user role of request
  user_roles = auth_m.users.list_roles(id=user_id)['roles']
  print('userroles:', user_roles)
  if len(list(filter(lambda x: x['name'] == 'Administrator', user_roles))) > 0:
    # user is an admin, cant update
    raise AuthError(description='User is an admin, cant update', code=403)
  
  # perform update
  try:
    auth_m.users.update(id=user_id, body={'username': new_username})
    return jsonify({
      'success': True,
      'message': 'Username updated'
    }), 201
  except:
    abort(500, description='Error updating username')


@user_bp.errorhandler(AuthError)
def handle_auth_error(exception: AuthError):
  return jsonify({
    'success': False,
    'code': exception.code,
    'error': exception.error,
    'message': exception.description
  }), exception.code
  
@user_bp.errorhandler(422)
def handle_422(error):
  # bad syntax
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Error in Query/Data",
      "error": 422
  }), 422


@user_bp.errorhandler(404)
def handle_404(error):
  # Not Found
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Resource not Found",
      "error": 404
  }), 404
  
@user_bp.errorhandler(400)
def handle_400(error):
  # Not Found
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Bad Syntax",
      "error": 400
  }), 400


@user_bp.errorhandler(405)
def handle_405(error):
  # Method Not Allowed
  return jsonify({
      "success": False,
      "message": "Method not allowed",
      "error": 405
  }), 405


@user_bp.errorhandler(503)
def handle_503(error):
  # Server cannot process the request
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "System Busy",
      "error": 503
  }), 503