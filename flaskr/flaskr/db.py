import os
import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(os.environ.get('DATABASE_URL'))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def get_db():
    if 'db' not in g:
        g.db = engine.connect()
        #g.db = connection()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    engine.execute('DROP TABLE IF EXISTS post')
    engine.execute('DROP TABLE IF EXISTS user_tb')
    import flaskr.models
    Base.metadata.create_all(bind=engine)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
