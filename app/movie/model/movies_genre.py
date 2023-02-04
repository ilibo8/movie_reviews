from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


class MovieGenre(Base):
    __tablename__ = "movie_genre"
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    genre_name = Column(String(20), ForeignKey("genres.name", ondelete="CASCADE"), primary_key=True)
    __table_args__ = (UniqueConstraint("movie_id", "genre_name", name="movie_genre_uc"),)

    movie = relationship("Movie", foreign_keys=movie_id, back_populates="movie_genre", lazy="subquery")
    genre = relationship("Genre", foreign_keys=genre_name, back_populates="movie_genre", lazy="subquery")

    def __init__(self, movie_id, genre_name):
        self.movie_id = movie_id
        self.genre_name = genre_name
