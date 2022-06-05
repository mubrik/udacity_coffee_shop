'''
  handler to start tests
'''
import os
import unittest
from dotenv import load_dotenv
from app.setup import create_app

# load env
load_dotenv()

# get test db uri
database_uri = os.environ.get('TEST_DB_URI')

# Define the WSGI application object
app, db = create_app(__name__, {
  'SQLALCHEMY_DATABASE_URI': database_uri,
  'SQLALCHEMY_ECHO': True,
  'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})
print("app testing init name:", __name__)

# import test cases
from app.auth.tests import AuthTestCase
from app.drink.tests import DrinkTestCase

if __name__ == '__main__':
  unittest.main()