'''
  holds the blueprint routes for drink
'''
from flask import Blueprint,request, jsonify, abort
import sqlalchemy
from .models import Drink
# auth decorators
from ..auth import requires_authentication, requires_authorization, AuthError
from app import db 

# drink bp
drink_bp = Blueprint('drink', __name__)

@drink_bp.route('/drink/test')
def test():
  # test
  return jsonify({'message': 'drink'})


@drink_bp.route('/drinks', methods=['GET'])
# @requires_authentication
def get_drinks():
  drinks = Drink.query.all()
  return jsonify({
    'success': True,
    'drinks': [drink.short() for drink in drinks]
  })
  

@drink_bp.route('/drinks-detail', methods=['GET'])
@requires_authorization('get:drinks-detail')
def get_drinks_detail(permission):
  drinks = Drink.query.all()
  return jsonify({
    'success': True,
    'drinks': [drink.format() for drink in drinks]
  })
  

@drink_bp.route('/drinks', methods=['POST'])
@requires_authorization('post:drinks')
def post_drink(permission):
  # get data from request
  data = request.get_json()
  # check if title is in data
  if 'title' not in data or 'recipe' not in data:
    return jsonify({
      'success': False,
      'message': 'title and recipe required'
    }), 400
  # create drink
  if type(data['recipe']) is dict:
    # postman data is json dict, edge case but watching it
    drink = Drink(title=data['title'], recipe=[data['recipe']])
  else:
    drink = Drink(title=data['title'], recipe=data['recipe'])
  # insert drink
  try:
    returned_data = drink.insert().format()
  except sqlalchemy.exc.IntegrityError:
    # failed to insert becaus not unique
    abort(422, "Title is not unique")
  except Exception as e:
    # other exception
    db.session.rollback()
    abort(500, "Internal server error")
  finally:
    db.session.close()
  # return drink
  return jsonify({
    'success': True,
    'drinks': [returned_data]
  }), 201
  
  
@drink_bp.route('/drinks/<int:id>', methods=['PATCH'])
@requires_authorization('patch:drinks')
def patch_drink(permission, id):
  # get data from request
  data = request.get_json()
  # check if title is in data, one of the two is required
  if 'title' not in data and 'recipe' not in data:
    return jsonify({
      'success': False,
      'message': 'title and recipe required'
    }), 400
    # get drink
  drink = Drink.query.filter(Drink.id == id).one_or_none()
  # check if drink exists
  if drink is None:
    return jsonify({
      'success': False,
      'message': 'drink not found'
    }), 404
  # update drink
  for key, value in data.items():
    setattr(drink, key, value)
  try:
    returned_data = drink.update().format()
  except sqlalchemy.exc.IntegrityError:
    # failed to update becaus not unique
    abort(422, "Recipe with that title already exists")
  except Exception as e:
    print(e)
    db.session.rollback()
    abort(500, "Internal server error")
  finally:
    db.session.close()
    
  # return drink
  return jsonify({
    'success': True,
    'drinks': [returned_data]
  })
  

@drink_bp.route('/drinks/<int:id>', methods=['DELETE'])
@requires_authorization('delete:drinks')
def delete_drink(permission, id):
  # get drink
  drink = Drink.query.filter(Drink.id == id).one_or_none()
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
    abort(500, "Internal server error")
  finally:
    db.session.close()
  # return drink
  return jsonify({
    'success': True,
    'delete': id
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
def handle_auth_error(exception):
  return jsonify({
    'success': False,
    'code': exception.code,
    'error': exception.error,
    'message': exception.description
  }), exception.code


@drink_bp.errorhandler(422)
def handle_422(error):
  # bad syntax
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Error in Query/Data",
      "error": 422
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
  
@drink_bp.errorhandler(400)
def handle_400(error):
  # Not Found
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Bad Syntax",
      "error": 400
  }), 400


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
      "message": error.description if error.description is not None else "System Busy",
      "error": 503
  }), 503
