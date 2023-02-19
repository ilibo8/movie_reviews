"""Module for Group repository testing"""

import pytest
from app.groups.exceptions import DuplicateEntry, GroupNotFound
from app.groups.repository import GroupRepository
from app.tests import TestClass, TestingSessionLocal
from app.users.repository import UserRepository


class TestGroupRepository(TestClass):
    """Class for testing methods for GroupRepository"""

    def create_foreign_keys(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user_repository.create_user("user1", "pass", "user1@gmail.com")
            user_repository.create_user("user2", "pass", "user2@gmail.com")
            user_repository.create_user("user3", "pass", "user3@gmail.com")

    def test_create_group(self):
        """Test method add_group."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            group = group_repository.add_group("romantic", 1, "some desc")
            assert group.group_name == "romantic"
            assert group.description == "some desc"
            assert group.id == 1

    def test_create_group_fail(self):
        """Test method add_group error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            group_repository.add_group("romantic", 1, "some desc")
            with pytest.raises(DuplicateEntry):
                group_repository.add_group("romantic", 1, "some other desc")

    def test_get_all(self):
        """Test for getting all groups."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            group_repository.add_group("romantic1", 1, "some desc")
            group_repository.add_group("romantic2", 1, "some desc")
            group_repository.add_group("romantic3", 1, "some desc")
            groups = group_repository.get_all()
            assert len(groups) == 3

    def test_get_group_by_name(self):
        """Test for method get_group_by_name."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            group_repository.add_group("name", 1, "description")
            group = group_repository.get_group_by_name("name")
            assert group.owner_id == 1
            assert group.description == "description"
            assert group.group_name == "name"

    def test_get_group_name_by_id(self):
        """Test for method get_group_name_by_id."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            group_repository.add_group("blue", 1, "description")
            assert group_repository.get_group_name_by_id(1) == "blue"

    def test_get_group_name_by_id_error(self):
        """Test method get_group_name_by_id error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            group_repository.add_group("romantic", 1, "some desc")
            with pytest.raises(GroupNotFound):
                group_repository.get_group_name_by_id(2)

    def test_get_group_id_by_name(self):
        """Test method get_group_id_by_name."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            group_repository.add_group("blue", 1, "description")
            group_repository.add_group("red", 1, "description")
            assert group_repository.get_group_id_by_name("red") == 2

    def test_get_group_id_by_name_error(self):
        """Test method get_group_id_by_name error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            group_repository.add_group("romantic", 1, "some desc")
            with pytest.raises(GroupNotFound):
                group_repository.get_group_id_by_name("red")

    def test_change_group_name(self):
        """Test method change_group_name."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            group_repository.add_group("blue", 1, "description")
            group_repository.change_group_name("blue", "red")
            assert group_repository.get_group_name_by_id(1) == "red"

    def test_change_group_name_error(self):
        """Test method change_group_name error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            group_repository.add_group("red", 1, "some desc")
            group_repository.add_group("blue", 1, "some desc")
            with pytest.raises(DuplicateEntry):
                group_repository.change_group_name("blue", "red")

    def test_delete_group_by_id(self):
        """Testing deleting group by id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            group = group_repository.add_group("red", 1, "some desc")
            assert group_repository.delete_group_by_id(group.id) is True

    def test_delete_group_by_id_false(self):
        """Testing deleting actor by id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            group_repository = GroupRepository(db)
            with pytest.raises(GroupNotFound):
                group_repository.delete_group_by_id(1)
