from sqlalchemy import Integer, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


class MovieCast(Base):
    __tablename__ = "movie_cast"
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id", ondelete="CASCADE"), primary_key=True)
    __table_args__ = (UniqueConstraint("movie_id", "actor_id", name="movie_cast_uc"),)

    movie = relationship("Movie", foreign_keys=movie_id, back_populates="movie_cast", lazy="subquery")
    actor = relationship("Actor", foreign_keys=actor_id, back_populates="movie_cast", lazy="subquery")

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id
