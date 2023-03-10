"""Module for User table"""
from sqlalchemy import Boolean, Column, String, Integer
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(50), unique=True)
    is_superuser = Column(Boolean, default=False)

    review = relationship("Review", cascade="all, delete-orphan", back_populates="user", lazy="subquery")
    group_user = relationship("GroupUser", cascade="all, delete-orphan", back_populates="user", lazy="joined")
    group = relationship("Group", cascade="all, delete-orphan", back_populates="user", lazy="joined")

    def __init__(self, user_name: str, password: str, email: str, is_superuser=False):
        self.user_name = user_name
        self.password = password
        self.email = email
        self.is_superuser = is_superuser
