from sqlalchemy import Integer, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base


class MovieCast(Base):
    __tablename__ = "movie_cast"
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"), primary_key=True)
    __table_args__ = (UniqueConstraint("movie_id", "actor_id", name="movie_cast_uc"), {"mysql_engine": "InnoDB"})

    movie = relationship("Movie", back_populates="movie_cast")
    actor = relationship("Actor", back_populates="movie_cast")

    def __init__(self, movie_id: int, actor_id: int):
        self.movie_id = movie_id
        self.actor_id = actor_id
