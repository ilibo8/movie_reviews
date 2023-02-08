from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


class MovieGenre(Base):
    __tablename__ = "movie_genre"
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    genre_name = Column(String(20), ForeignKey("genres.name"), primary_key=True)
    __table_args__ = (UniqueConstraint("movie_id", "genre_name", name="movie_genre_uc"), {'mysql_engine': 'InnoDB'})

    movie = relationship("Movie", back_populates="movie_genre")
    genre = relationship("Genre", back_populates="movie_genre")

    def __init__(self, movie_id, genre_name):
        self.movie_id = movie_id
        self.genre_name = genre_name
