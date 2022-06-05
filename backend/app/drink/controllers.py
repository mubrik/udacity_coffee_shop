'''
  holds the blueprint routes for drink
'''
from typing import List
from flask import Blueprint,request, jsonify
from .models import Drink
# auth decorators
from ..auth import requires_authentication, requires_authorization, AuthError
from app import db 

# drink bp
drink_bp = Blueprint('drink', __name__)

@drink_bp.after_request
def after(response):
  # add to headers after controllers
  response.headers.add('Access-Control-Allow-Headers',
                       'Content-Type,Authorization,true')
  response.headers.add('Access-Control-Allow-Methods',
                       'GET,PATCH,POST,DELETE')
  return response

@drink_bp.route('/test')
def test():
  # test
  return jsonify({'message': 'drink'})


@drink_bp.route('/drinks', methods=['GET'])
@requires_authentication
def get_drinks():
  drinks: List[Drink] = Drink.query.all()
  return jsonify({
    'success': True,
    'drinks': [drink.short() for drink in drinks]
  })
  

@drink_bp.route('/drinks-detail', methods=['GET'])
@requires_authorization('get:drinks-detail')
def get_drinks_detail():
  drinks: List[Drink] = Drink.query.all()
  return jsonify({
    'success': True,
    'drinks': [drink.format() for drink in drinks]
  })
  

@drink_bp.route('/drinks', methods=['POST'])
@requires_authorization('post:drinks')
def post_drink():
  # get data from request
  data = request.get_json()
  # check if title is in data
  if 'title' not in data or 'recipe' not in data:
    return jsonify({
      'success': False,
      'message': 'title and recipe required'
    }), 400
    # create drink
  drink = Drink(title=data['title'], recipe=data['recipe'])
  # insert drink
  try:
    returned_data = drink.insert().format()
  except Exception as e:
    print(e)
    db.session.rollback()
  finally:
    db.session.close()
  # return drink
  return jsonify({
    'success': True,
    'drinks': [returned_data]
  }), 201
  
  
@drink_bp.route('/drinks/<int:id>', methods=['PATCH'])
@requires_authorization('patch:drinks')
def patch_drink(id):
  # get data from request
  data = request.get_json()
  # check if title is in data
  if 'title' not in data or 'recipe' not in data:
    return jsonify({
      'success': False,
      'message': 'title and recipe required'
    }), 400
    # get drink
  drink: Drink|None = Drink.query.filter(Drink.id == id).one_or_none()
  # check if drink exists
  if drink is None:
    return jsonify({
      'success': False,
      'message': 'drink not found'
    }), 404
    # update drink
  drink.title = data['title']
  drink.recipe = data['recipe']
  try:
    returned_data = drink.update().format()
  except Exception as e:
    print(e)
    db.session.rollback()
  finally:
    db.session.close()
    
  # return drink
  return jsonify({
    'success': True,
    'drinks': [returned_data]
  })
  

@drink_bp.route('/drinks/<int:id>', methods=['DELETE'])
@requires_authorization('delete:drinks')
def delete_drink(id):
  # get drink
  drink: Drink|None = Drink.query.filter(Drink.id == id).one_or_none()
  # check if drink exists
  if drink is None:
    return jsonify({
      'success': False,
      'message': 'drink not found'
    }), 404
  # delete drink
  try:
    drink.delete()
  except Exception as e:
    print(e)
    db.session.rollback()
  finally:
    db.session.close()
  # return drink
  return jsonify({
    'success': True,
    'drinks': id
  })

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# Error Handling
'''
Example error handling for unprocessable entity
'''

@drink_bp.errorhandler(AuthError)
def handle_auth_error(exception: AuthError):
  response = jsonify({
    'success': False,
    'code': exception.error['code'],
    'error': exception.error['error'],
    'message': exception.error['description']
  })
  response.status_code = exception.error['code']
  return response


@drink_bp.errorhandler(422)
def unprocessable(error):
  return jsonify({
    "success": False,
    "error": 422,
    "message": "unprocessable"
  }), 422


@drink_bp.errorhandler(404)
def handle_404(error):
  # Not Found
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Resource not Found",
      "error": 404
  }), 404


@drink_bp.errorhandler(405)
def handle_405(error):
  # Method Not Allowed
  return jsonify({
      "success": False,
      "message": "Method not allowed",
      "error": 405
  }), 405


@drink_bp.errorhandler(503)
def handle_503(error):
  # Server cannot process the request
  return jsonify({
      "success": False,
      "message": "System Busy",
      "error": 503
  }), 503
