from sqlalchemy.orm import Session

from app.groups.exceptions import GroupNotFoundException
from app.groups.model import Group


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_group(self, name: str, owner_user_name: str, description: str):
        try:
            group = Group(name, owner_user_name, description)
            self.db.add(group)
            self.db.commit()
            self.db.refresh(group)
            print("!!!!!!!!", group)
            return group
        except Exception as e:
            raise e

    def get_all(self):
        try:
            if self.db.query(Group).first() is None:
                raise GroupNotFoundException("Group table has no data.")
            groups = self.db.query(Group).all()
            return groups
        except Exception as e:
            raise e

    def delete_group_by_id(self, group_id: int) -> bool:
        group = self.db.query(Group).filter(Group.id == group_id).first()
        if group is None:
            return False
        self.db.delete(group)
        self.db.commit()
        return True
