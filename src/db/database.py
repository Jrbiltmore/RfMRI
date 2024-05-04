
# /RfMRI/src/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from src.config import get_config

config = get_config()

engine = create_engine(config.DATABASE_URI, pool_size=20, max_overflow=0, echo=config.DEBUG, client_encoding='utf8')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """Import all modules here that might define models so that
    they will be registered properly on the metadata. Otherwise
    you will have to import them before calling init_db()."""
    from src.models import User, MRIAnalysis  # Import all the models
    Base.metadata.create_all(bind=engine)

def initialize_db(database_uri):
    """Initialize the database with the given URI, setting up a new engine if necessary."""
    global engine, db_session
    if engine.url != database_uri:
        engine = create_engine(database_uri, pool_size=20, max_overflow=0, echo=config.DEBUG, client_encoding='utf8')
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        Base.metadata.bind = engine
        Base.metadata.create_all(bind=engine)

def shutdown_db_session(exception=None):
    """Close the database session, ensuring all resources are freed properly."""
    db_session.remove()

def commit_changes():
    """Commit the current transaction."""
    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e

def add_entity(entity):
    """Add a new entity to the database session."""
    db_session.add(entity)
    commit_changes()

def delete_entity(entity):
    """Delete an entity from the database session."""
    db_session.delete(entity)
    commit_changes()
