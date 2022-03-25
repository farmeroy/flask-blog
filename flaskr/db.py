import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    # g is an object that is unique for each request
    # g stores request specific data
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
                )
        # returns rows that behave like dicts
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    # open_resource() opens a file relative to flaskr
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# click.command() defines a CL command called init-db that calls 
# the init_db function
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    # tell flask to call a function when cleaning up
    # aftre a response
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


