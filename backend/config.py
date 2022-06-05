import os
from dotenv import load_dotenv

# loadenv variable
load_dotenv()

# Statement for enabling the development environment
DEBUG = os.environ.get("DEBUG", True)

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
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