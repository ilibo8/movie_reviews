from sqlalchemy.orm import relationship

from app.db.database import Base
from sqlalchemy import Column, String


class Genre(Base):
    __tablename__ = "genres"
    name = Column(String(20), unique=True, primary_key=True)

    movie_genre = relationship("MovieGenre", back_populates="genre", lazy="subquery")

    def __init__(self, name):
        self.name = name
