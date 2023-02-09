from app.db import SessionLocal
from app.groups.exceptions import GroupNotFoundException
from app.groups.repository import GroupRepository


class GroupService:

    @staticmethod
    def add_group(name: str, owner_user_name: str, description: str):
        with SessionLocal() as db:
            try:
                group_repository = GroupRepository(db)
                return group_repository.add_group(name, owner_user_name, description)
            except Exception as e:
                raise e

    @staticmethod
    def get_all():
        try:
            with SessionLocal as db:
                group_repository = GroupRepository(db)
                groups = group_repository.get_all()
                print(groups)
                if len(groups) == 0:
                    raise GroupNotFoundException("No groups created yet.")
                return groups
        except Exception as e:
            raise e

    @staticmethod
    def delete_by_id(group_id: int):
        try:
            with SessionLocal as db:
                group_repository = GroupRepository(db)
                if group_repository.delete_group_by_id(group_id):
                    return True
                raise GroupNotFoundException(f"No group with id {group_id}")
        except Exception as e:
            raise e
