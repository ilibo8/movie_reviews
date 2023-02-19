"""Module for Group model"""
from datetime import date
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date
from app.db import Base


class Group(Base):
    __tablename__ = "movie_groups"
    id = Column(Integer, primary_key=True)
    group_name = Column(String(30), unique=True)
    owner_id = Column(Integer)
    description = Column(String(100))
    date_created = Column(Date, nullable=False)

    group_user = relationship("GroupUser", cascade="all, delete-orphan", back_populates="movie_group", lazy="joined")

    def __init__(self, group_name: str, owner_id: int, description: str, date_created: str = date.today()):
        self.group_name = group_name
        self.owner_id = owner_id
        self.description = description
        self.date_created = date_created
