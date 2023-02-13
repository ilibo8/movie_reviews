from uuid import uuid4

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, UniqueConstraint, ForeignKey, CheckConstraint
from app.db import Base


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
    user_id = Column(String(50), ForeignKey("users.id"))
    rating_number = Column(Integer, nullable=False)
    rating_description = Column(String(1000))
    __table_args__ = (CheckConstraint("0 < rating_number <= 10"),
                      UniqueConstraint("movie_id", "user_id", name="review_uc"),
                      {"mysql_engine": "InnoDB"})

    movie = relationship("Movie", back_populates="review")
    user = relationship("User", back_populates="review")

    def __init__(self, movie_id, user_id, rating_number, rating_description):
        self.movie_id = movie_id
        self.user_id = user_id
        self.rating_number = rating_number
        self.rating_description = rating_description