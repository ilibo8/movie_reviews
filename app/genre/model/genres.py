"""Module for Genre Model"""
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from app.db import Base


class Genre(Base):
    __tablename__ = "genres"
    name = Column(String(20), unique=True, primary_key=True)

    movie_genre = relationship("MovieGenre", cascade="all, delete-orphan", back_populates="genre")

    def __init__(self, name: str):
        self.name = name
