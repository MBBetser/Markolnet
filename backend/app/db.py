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

