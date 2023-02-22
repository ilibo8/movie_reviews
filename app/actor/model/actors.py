"""Module for Actor table"""
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer
from app.db import Base


class Actor(Base):
    """Class for table actors"""
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(50))
    nationality = Column(String(50))

    movie_cast = relationship("MovieCast", cascade="all, delete-orphan", back_populates="actor", lazy="subquery")

    def __init__(self, full_name: str, nationality: str):
        self.full_name = full_name
        self.nationality = nationality
