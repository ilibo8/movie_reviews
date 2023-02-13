from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer
from app.db import Base


class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(50))
    nationality = Column(String(50))

    movie_cast = relationship("MovieCast", back_populates="actor")

    def __init__(self, full_name: str, nationality: str):
        self.full_name = full_name
        self.nationality = nationality
