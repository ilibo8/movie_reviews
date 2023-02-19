"""Module for testing GroupUser repository"""
import pytest
from sqlalchemy.exc import IntegrityError
from app.groups.exceptions import DuplicateEntry, GroupUserNotFound
from app.groups.repository import GroupUserRepository, GroupRepository
from app.tests import TestClass, TestingSessionLocal
from app.users.repository import UserRepository


class TestGroupUserRepository(TestClass):
    """Class for testing GroupUser repository"""

    def create_foreign_keys(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            group_repository = GroupRepository(db)
            user_repository.create_user("user1", "pass", "user1@gmail.com")
            user_repository.create_user("user2", "pass", "user2@gmail.com")
            user_repository.create_user("user3", "pass", "user3@gmail.com")
            group_repository.add_group("g1", 1, "desc")
            group_repository.add_group("g2", 1, "desc")
            group_repository.add_group("g3", 3, "desc")

    def test_add_group_user(self):
        """Test method add_group_user"""
        with TestingSessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            self.create_foreign_keys()
            group_user_repository.add_group_user(group_id=1, user_id=2)
            assert group_user_repository.check_if_user_is_part_of_group("g1", 2)

    def test_add_group_user_error(self):
        """Test method add_group_user error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            group_user_repository.add_group_user(group_id=1, user_id=2)
            with pytest.raises(DuplicateEntry):
                group_user_repository.add_group_user(group_id=1, user_id=2)

    def test_add_group_user_integrity_error(self):
        """Test method add_group_user integrity error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            with pytest.raises(IntegrityError):
                group_user_repository.add_group_user(group_id=3, user_id=7)

    def test_add_group_user_integrity_error2(self):
        """Test method add_group_user integrity error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            with pytest.raises(IntegrityError):
                group_user_repository.add_group_user(group_id=4, user_id=3)

    def test_get_all(self):
        """Test method get all group users"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            group_user_repository.add_group_user(group_id=1, user_id=2)
            group_user_repository.add_group_user(group_id=2, user_id=2)
            group_users = group_user_repository.get_all()
            assert len(group_users) == 5

    def test_get_all_group_members_ids(self):
        """Testing getting all group members ids"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            group_user_repository.add_group_user(group_id=1, user_id=2)
            group_user_repository.add_group_user(group_id=2, user_id=2)
            group_user_repository.add_group_user(group_id=1, user_id=3)
            assert group_user_repository.get_all_group_members_ids(group_id=1) == [1, 2, 3]

    def test_get_id_by_user_and_group_id(self):
        """Testing method get_id_by_user_and_group_id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            group_user_repository.add_group_user(3, 2)
            assert group_user_repository.get_id_by_user_and_group_id(1, 1) == 1
            assert group_user_repository.get_id_by_user_and_group_id(2, 1) == 2
            assert group_user_repository.get_id_by_user_and_group_id(3, 2) == 4

    def test_get_id_by_user_and_group_id_error(self):
        """Testing method get_id_by_user_and_group_id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            with pytest.raises(GroupUserNotFound):
                group_user_repository.get_id_by_user_and_group_id(1, 2)

    def test_get_user_name_by_group_user_id(self):
        """Testing method get_user_name_by_group_user_id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            group_user_repository.add_group_user(3, 2)
            assert group_user_repository.get_user_name_by_group_user_id(1) == "user1"
            assert group_user_repository.get_user_name_by_group_user_id(2) == "user1"
            assert group_user_repository.get_user_name_by_group_user_id(4) == "user2"

    def test_get_user_name_by_group_user_id_error(self):
        """Testing method get_user_name_by_group_user_id error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            with pytest.raises(GroupUserNotFound):
                group_user_repository.get_user_name_by_group_user_id(4)

    def test_check_if_user_is_part_of_group_error(self):
        """Testing errors for method check_if_user_is_part_of_group"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            with pytest.raises(GroupUserNotFound):
                group_user_repository.check_if_user_is_part_of_group("some name", 2)

    def test_check_if_user_is_part_of_group(self):
        """Testing method check_if_user_is_part_of_group"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            assert group_user_repository.check_if_user_is_part_of_group("g1", 1) is True
            assert group_user_repository.check_if_user_is_part_of_group("g2", 1) is True
            assert group_user_repository.check_if_user_is_part_of_group("g3", 3) is True
            assert group_user_repository.check_if_user_is_part_of_group("g2", 3) is False
            assert group_user_repository.check_if_user_is_part_of_group("g3", 1) is False

    def test_delete_group_user(self):
        """Testing deleting group user"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            assert group_user_repository.delete_group_user(group_id=1, user_id=1) is True

    def test_delete_group_user_false(self):
        """Testing error when deleting group user"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            assert group_user_repository.delete_group_user(group_id=1, user_id=2) is False
