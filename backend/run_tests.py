'''
  handler to start tests
'''
import sys, unittest

# add args to sys.path
sys.argv.append('--testApp')

# import app
from app import *

# import test cases
from app.user.tests import UserTestCase
from app.drink.tests import DrinkTestCase

if __name__ == '__main__':
  sys.argv.remove('--testApp')
  unittest.main(verbosity=2)
  pass