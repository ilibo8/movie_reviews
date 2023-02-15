"""Module for testing GroupUser repository"""
import pytest
from sqlalchemy.exc import IntegrityError

from app.groups.exceptions import DuplicateEntry
from app.groups.repository import GroupUserRepository, GroupRepository
from app.tests import TestClass, TestingSessionLocal
from app.users.repository import UserRepository


class TestGroupUserRepository(TestClass):
    """Class for testing GroupUser repository"""

    def create_foreign_keys(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            group_repository = GroupRepository(db)
            group_repository.add_group("g1", "desc")
            group_repository.add_group("g2", "desc")
            user_repository.create_user("user1", "pass", "user1@gmail.com")
            user_repository.create_user("user2", "pass", "user2@gmail.com")
            user_repository.create_user("user3", "pass", "user3@gmail.com")

    def test_add_group_user(self):
        """Test method add_group_user"""
        with TestingSessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            self.create_foreign_keys()
            group = group_user_repository.add_group_user(group_id=1, user_id=1)
            assert group.group_id == 1
            assert group.user_id == 1

    def test_add_group_user_error(self):
        """Test method add_group_user error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            group_user_repository.add_group_user(group_id=1, user_id=1)
            with pytest.raises(DuplicateEntry):
                group_user_repository.add_group_user(group_id=1, user_id=1)

    def test_add_group_user_integrity_error(self):
        """Test method add_group_user integrity error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            with pytest.raises(IntegrityError):
                group_user_repository.add_group_user(group_id=3, user_id=4)

    def test_get_all_group_users(self):
        """Method for testing getting all groups and their users."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            group_user_repository.add_group_user(group_id=1, user_id=1)
            group_user_repository.add_group_user(group_id=2, user_id=1)
            group_user_repository.add_group_user(group_id=1, user_id=2)
            assert len(group_user_repository.get_all()) == 3

    def test_get_all_group_members(self):
        """Testing getting all group members"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            group_user_repository.add_group_user(group_id=1, user_id=1)
            group_user_repository.add_group_user(group_id=2, user_id=1)
            group_user_repository.add_group_user(group_id=1, user_id=2)
            members = group_user_repository.get_all_group_members(group_id=1)
            assert len(members) == 2

    def test_delete_group_user(self):
        """Testing deleting group user"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            group_user_repository.add_group_user(group_id=1, user_id=1)
            assert group_user_repository.delete_group_user(group_id=1, user_id=1) is True

    def test_delete_group_user_false(self):
        """Testing error when deleting group user"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_user_repository = GroupUserRepository(db)
            assert group_user_repository.delete_group_user(group_id=1, user_id=1) is False
