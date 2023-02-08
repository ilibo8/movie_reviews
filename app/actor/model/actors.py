from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy import Column, String, Integer


class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(50))
    nationality = Column(String(50))

    movie_cast = relationship("MovieCast", back_populates="actor", lazy="joined")

    def __init__(self, full_name, nationality):
        self.full_name = full_name
        self.nationality = nationality
