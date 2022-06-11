'''
  holds test cases for the user module
'''
import unittest
from app import app, db
from dotenv import load_dotenv
from os import environ as env
import http.client

# loadenv .env
load_dotenv()

# get env variables
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
API_AUDIENCE = env.get("API_AUDIENCE")
CLIENT_ID=env.get("AUTH0_CLIENT_ID")
CLIENT_SECRET=env.get("AUTH0_CLIENT_SECRET")
ALGORITHMS = env.get("ALGORITHMS", ['RS256'])

# implement uittest later

class UserTestCase(unittest.TestCase):
  '''
    base class for user tests
  '''
  def setUp(self):
    '''
      set up
      Define test variables and initialize app.
    '''
    app.testing = True
    self.app = app
    self.client = self.app.test_client
    # binds the app to the current context
    with self.app.app_context():
      self.db = db 
      # create all tables
      self.db.create_all()
    pass


  def tearDown(self):
    '''
      tear down
    '''
    pass
  
  
  def test_basic_route(self):
    '''
      test something
    '''
    result = self.client().get('/api/users/test')
    self.assertEqual(result.status_code, 200)
    self.assertIn('test', result.json['message'])
    
  