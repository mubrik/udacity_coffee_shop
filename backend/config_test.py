import os
from dotenv import load_dotenv

# loadenv variable
load_dotenv()

# Statement for enabling the development environment
DEBUG = os.environ.get("DEBUG", False) # false for testing

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'coffee_shop_tests.db')

# Define the database - we are working with
# SQLLITE_DB for sql lite, DB_URI for postgres
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
# print queries if debug
SQLALCHEMY_ECHO = True if DEBUG else False
# over head
SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies, not secure.. testing only
SECRET_KEY = os.urandom(32)