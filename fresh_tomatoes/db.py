from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import *


def connect(app):
    """Connects to the specific database."""
    engine = create_engine(app.config['DATABASE'], echo=True)
    Session = sessionmaker(bind=engine)
    return engine, Session


def get(app, g):
    """Opens a singleton database connection for the current application
    context.
    """
    if not hasattr(g, 'db_engine'):
        g.db_engine, g.db_Session = connect(app)
    return g.db_engine, g.db_Session


def init(app, g):
    """Initializes the application database."""
    engine, _ = get(app, g)
    Base.metadata.create_all(engine)


def load_sample_data(app, g, data):
    """Loads sample data into the database."""
    _, Session = get(app, g)
    session = Session()
    try:
        for fields in data['movies']:
            movie = Movie(**fields)
            session.add(movie)
        session.commit()
    except err:
        session.rollback()
        raise err
    finally:
        session.close()


def list_movies(app, g):
    """Lists movies in the database."""
    _, Session = get(app, g)
    session = Session()
    try:
        query = session.query(Movie).order_by(Movie.title)
    finally:
        session.close()
    return query.all()


def add_movie(app, g, **kwargs):
    """Adds a movie to the database."""
    _, Session = get(app, g)
    session = Session()
    try:
        movie = Movie(**kwargs)
        session.add(movie)
        session.commit()
    except err:
        session.rollback()
        raise err
    finally:
        session.close()


def remove_movie(app, g, movie_id):
    """Removes a movie from the database by ID."""
    _, Session = get(app, g)
    session = Session()
    try:
        session.query(Movie).filter(Movie.id == movie_id).delete()
        session.commit()
    except err:
        session.rollback()
        raise err
    finally:
        session.close()
