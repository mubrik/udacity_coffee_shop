'''
  init file, set up the app
'''
from .setup import create_app

# Define the WSGI application object
app, db = create_app(__name__, None)

# Import a module / component using its blueprint handler variable (mod_auth)
from .auth.controllers import auth_bp as authentication_blueprint
from .drink.controllers import drink_bp as drink_blueprint

# Register blueprint(s)
app.register_blueprint(authentication_blueprint, url_prefix='/api/auth')
app.register_blueprint(drink_blueprint, url_prefix='/api')

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

