"""Module for Movie model"""
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, UniqueConstraint, Float

from app.db import Base


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    director = Column(String(50))
    release_year = Column(Integer)
    country_of_origin = Column(String(50))
    average_rating = Column(Float)
    number_of_ratings = Column(Integer)
    __table_args__ = (UniqueConstraint("title", "director", "release_year", "country_of_origin", name="movie_uc"),)

    movie_cast = relationship("MovieCast", cascade="all, delete-orphan", back_populates="movie", lazy="joined")
    movie_genre = relationship("MovieGenre", cascade="all, delete-orphan", back_populates="movie", lazy="joined")
    review = relationship("Review", cascade="all, delete-orphan", back_populates="movie", lazy="joined")

    def __init__(self, title: str, director: str, release_year: int, country_of_origin: str, average_rating=None,
                 number_of_ratings=None):
        self.title = title
        self.director = director
        self.release_year = release_year
        self.country_of_origin = country_of_origin
        self.average_rating = average_rating
        self.number_of_ratings = number_of_ratings
