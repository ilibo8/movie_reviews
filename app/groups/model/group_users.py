"""Module for GroupUser model"""
from sqlalchemy import Integer, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base


class GroupUser(Base):
    """Model for GroupUser table"""
    __tablename__ = "groups_users"
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    __table_args__ = (UniqueConstraint("group_id", "user_id", name="group_user_uc"),)

    group = relationship("Group", back_populates="group_user")
    user = relationship("User", back_populates="group_user")

    def __init__(self, group_id: int, user_id: int):
        self.group_id = group_id
        self.user_id = user_id

