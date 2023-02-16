"""Module for model Recommendation."""
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey
from app.db import Base


class Recommendation(Base):
    """Class for creating Recommendation table."""
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True)
    group_user_id = Column(Integer, ForeignKey("groups_users.id", ondelete="CASCADE"))
    post = Column(String(500))

    group_user = relationship("GroupUser", back_populates="recommendations")

    def __init__(self, group_user_id: int, post: str):
        self.group_user_id = group_user_id
        self.post = post

