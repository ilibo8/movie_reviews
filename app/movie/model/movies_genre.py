"""Module for MovieGenre model"""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base


class MovieGenre(Base):
    __tablename__ = "movie_genre"
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    genre_name = Column(String(20), ForeignKey("genres.name",ondelete="CASCADE"), primary_key=True)
    __table_args__ = (UniqueConstraint("movie_id", "genre_name", name="movie_genre_uc"),)

    movie = relationship("Movie", back_populates="movie_genre")
    genre = relationship("Genre", back_populates="movie_genre")

    def __init__(self, movie_id: int, genre_name: str):
        self.movie_id = movie_id
        self.genre_name = genre_name
