from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime

from app.db import Base


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    owner_user_name = Column(String(50))
    description = Column(String(100))
    date_created = Column(String(10))
    __table_args__ = ({"mysql_engine": "InnoDB"})

    def __init__(self, name: str, owner_user_name: str, description: str):
        self.name = name
        self.owner_user_name = owner_user_name
        self.description = description
        self.date_created = datetime.now().strftime("%d-%m-%Y")
