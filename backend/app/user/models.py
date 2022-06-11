'''
  Models for auth
'''
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  '''
    base class for inheritance of id and dates
    very thin just for testing
  '''
  __abstract__  = True

  id = db.Column(db.Integer, primary_key=True)
  date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                      onupdate=db.func.current_timestamp())


class User(Base):
  '''
    User Model Base
  '''
  __tablename__ = 'users'


  name = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), nullable=False, unique=True)

  def __init__(self, name, email):
    self.name = name
    self.email = email

  def __repr__(self):
    return f'<User id:{self.id} name:{self.name}>'