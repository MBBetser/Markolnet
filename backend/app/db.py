from flask_sqlalchemy import SQLAlchemy
import click
from flask import current_app, g

db = SQLAlchemy()

def init_db(app):
    """Clear the existing data and create new tables."""
    with app.app_context():
        db.drop_all()
        db.create_all()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db(current_app)
    click.echo('Initialized the database.')

def close_db(e=None):
    """Close the database session."""
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.remove()

def init_app(app):
    db.init_app(app)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# from flask import current_app, g
# import sqlite3
# import click


# def get_connection():
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row

#     return g.db

# def close_db(e=None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()


# def init_db():
#     db = get_connection()
#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))


# @click.command('init-db')
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')

# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)

     