'''
  init file, set up the app/tests
'''
import sys, os, unittest
from dotenv import load_dotenv
from typing import Dict, Tuple
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# load env
load_dotenv()

# create app function
def create_app(name="app", config: None|Dict=None, testing=False) -> Tuple[Flask, SQLAlchemy]:
  '''
    creates app, accepts name and config
    config allows for passing testing configs
  '''
  app = Flask(name)
  if config:
    print("testing")
    app.config.from_mapping(config)
  elif testing:
    print("testing")
    app.config.from_object('config_test')
  else:
    print("not testing")
    # get from config.py
    app.config.from_object('config')
    
  # Define the database object
  db = SQLAlchemy(app)
  # setup migration
  migrate = Migrate(app, db)
  # setup cors for api routes and specific origin
  cors = CORS(app, resources={r"/api/*": {"CORS_ORIGINS": "http://127.0.0.1:3000/"}})
  # return
  return [app, db]

# check testApp arg
if '--testApp' in sys.argv:
  # get test db uri
  # database_uri = os.environ.get('TEST_DB_URI')
  # sqllite_database_uri = os.environ.get('TEST_SQLITEDB_URI')
  # {
  #   'SQLALCHEMY_DATABASE_URI': sqllite_database_uri,
  #   'SQLALCHEMY_ECHO': True,
  #   'SQLALCHEMY_TRACK_MODIFICATIONS': False,
  # }
  # Define the WSGI application object
  app, db = create_app(__name__, testing=True)
  
else:
  # Define the WSGI application object
  app, db = create_app(__name__, None)

# Import a module / component using its blueprint handler variable (mod_auth)
from .user.controllers import user_bp as user_blueprint
from .drink.controllers import drink_bp as drink_blueprint

# Register blueprint(s)
app.register_blueprint(user_blueprint, url_prefix='/api')
app.register_blueprint(drink_blueprint, url_prefix='/api')

# Build the database, This will create the database file using SQLAlchemy
# check testApp arg
if '--testApp' not in sys.argv: db.create_all()

# app = None
# db = None

# # create_app func for cli args
# def create_cliapp(param: str):
#   global app 
#   global db
  
#   app = Flask(__name__)
#   if param == 'test':
#     print("testing")
#     app.config.from_object('config_test')
#   elif param == 'dev':
#     print("not testing")
#     # get from config.py
#     app.config.from_object('config')
    
#   # Define the database object
#   db = SQLAlchemy(app)
#   # setup migration
#   migrate = Migrate(app, db)
#   # setup cors for api routes and specific origin
#   cors = CORS(app, resources={r"/api/*": {"CORS_ORIGINS": "http://127.0.0.1:3000/"}})
  
#   # Import a module / component using its blueprint handler variable (mod_auth)
#   from .auth.controllers import auth_bp as authentication_blueprint
#   from .drink.controllers import drink_bp as drink_blueprint

#   # Register blueprint(s)
#   app.register_blueprint(authentication_blueprint, url_prefix='/api/auth')
#   app.register_blueprint(drink_blueprint, url_prefix='/api')
  
#   if param == 'test':
#     # import test cases
#     from .auth.tests import AuthTestCase
#     from .drink.tests import DrinkTestCase
    
#     # start test
#     unittest.main(verbosity=2)
  
#   return app

