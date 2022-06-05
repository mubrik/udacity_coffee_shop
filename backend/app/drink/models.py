'''
  Models for drink
'''
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  '''
    base class for inheritance of id and dates
  '''
  __abstract__  = True

  id = db.Column(db.Integer, primary_key=True)
  date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                onupdate=db.func.current_timestamp())


class Drink(Base):
  '''
    Drink Model
  '''
  __tablename__ = 'drinks'

  title = db.Column(db.String(80), nullable=False, unique=True)
  recipe = db.Column(db.PickleType, default=[], nullable=False)

  def __init__(self, title, recipe):
    self.title = title
    self.recipe = recipe
  
  '''
    insert()
    inserts a new model into a database
    the model must have a unique name
    the model must have a unique id or null id
    EXAMPLE
      drink = Drink(title=req_title, recipe=req_recipe)
      drink.insert()
  '''

  def insert(self):
    db.session.add(self)
    db.session.commit()
    return self

  '''
    delete()
    deletes a new model into a database
    the model must exist in the database
    EXAMPLE
      drink = Drink(title=req_title, recipe=req_recipe)
      drink.delete()
  '''

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  update()
    updates a new model into a database
    the model must exist in the database
    EXAMPLE
      drink = Drink.query.filter(Drink.id == id).one_or_none()
      drink.title = 'Black Coffee'
      drink.update()
  '''

  def update(self):
    db.session.commit()
    return self
  
  def short(self):
    short_recipe = [
      {'color': rec['color'], 'parts': rec['parts']} for rec in self.recipe
    ]
    return {
      'id': self.id,
      'title': self.title,
      'recipe': short_recipe
    }
    
  def long(self):
    return {
      'id': self.id,
      'title': self.title,
      'recipe': self.recipe
    }
    
  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'recipe': self.recipe
    }

  def __repr__(self):
    return f'<Drink id:{self.id} title:{self.title}>'