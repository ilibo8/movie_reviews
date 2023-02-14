from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, UniqueConstraint
from app.db import Base


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    director = Column(String(50))
    release_year = Column(Integer)
    country_of_origin = Column(String(50))
    __table_args__ = (UniqueConstraint("title", "director", "release_year", "country_of_origin", name="movie_uc"),)

    movie_cast = relationship("MovieCast", back_populates="movie", lazy="subquery")
    movie_genre = relationship("MovieGenre", back_populates="movie", lazy="subquery")
    review = relationship("Review", back_populates="movie", lazy="subquery")

    def __init__(self, title: str, director: str, release_year: int, country_of_origin: str):
        self.title = title
        self.director = director
        self.release_year = release_year
        self.country_of_origin = country_of_origin
