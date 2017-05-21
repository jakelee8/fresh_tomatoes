from sqlalchemy import Column, Date, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Movie(Base):
    """Movie ORM class.

    Attributes:
        id: A unique integer representing the movie.
        title: The movie title.
        image_uri: A URI to a poster for the movie.
        embed_uri: A URI to a YouTube embedded video for the movie.
        release_date: A datetime.Date instance for the movie release date.
    """

    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    image_uri = Column(String)
    embed_uri = Column(String)
    release_date = Column(Date)
