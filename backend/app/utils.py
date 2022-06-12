import click
from flask.cli import AppGroup
from app import app, db
from .drink.models import Drink

# create a cli group
app_cli = AppGroup('app')

@app_cli.command('dbtables')
@click.argument('action')
def db_tables(action='create'):
  if action == 'create':
    db.create_all()
  elif action == 'drop':
    db.drop_all()
    

@app_cli.command('dbrows')
@click.argument('action')
def db_tables(action='create'):
  new_drinks =['drink 1', 'drink 2', 'drink 3']
  if action == 'create':
    for value, index in enumerate(new_drinks):
      drink = Drink(title='title {}'.format(value), recipe=[{'color': 'blue', 'name': 'name {}'.format(value), 'parts': 'parts {}'.format(index)}])
      db.session.add(drink)
    db.session.commit()
  elif action == 'drop':
    Drink.query.delete()
    db.session.commit()
  elif action == 'get':
    print(Drink.query.all())
    
app.cli.add_command(app_cli)