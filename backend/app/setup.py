'''
  holds function for creating app
'''
from typing import Dict, List, Tuple
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

def create_app(name="app", config: None|Dict=None) -> Tuple[Flask, SQLAlchemy]:
  '''
    creates app, accepts name and config
    config allows for passing testing config
  '''
  app = Flask(name)
  if config:
    print("testing")
    app.config.from_mapping(config)
  else:
    print("not testing")
    # get from config.py
    app.config.from_object('config')
    
  # Define the database object
  db = SQLAlchemy(app)
  # setup migration
  migrate = Migrate(app, db)
  # setup cors
  cors = CORS(app, resources={"r*/api/*": {"origins": "*"}})
  # return
  return [app, db]
  
  