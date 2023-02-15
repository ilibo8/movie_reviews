"""Module for Group repository testing"""

import pytest

from app.groups.exceptions import DuplicateEntry
from app.groups.repository import GroupRepository
from app.tests import TestClass, TestingSessionLocal


class TestGroupRepository(TestClass):
    """Class for testing methods for GroupRepository"""
#####################################################
    def test_create_group(self):
        """Test method add_group."""
        with TestingSessionLocal() as db:
            group_repository = GroupRepository(db)
            group = group_repository.add_group("romantic", 1, "some desc")
            assert group.group_name == "romantic"
            assert group.description == "some desc"
            assert group.id == 1

    def test_create_group_fail(self):
        """Test method add_group error"""
        with TestingSessionLocal() as db:
            group_repository = GroupRepository(db)
            group_repository.add_group("romantic", 1, "some desc")
            with pytest.raises(DuplicateEntry):
                group_repository.add_group("romantic", 1, "some other desc")

    def test_get_all(self):
        """Test for getting all groups."""
        with TestingSessionLocal() as db:
            group_repository = GroupRepository(db)
            group_repository.add_group("romantic1", 1, "some desc")
            group_repository.add_group("romantic2", 1, "some desc")
            group_repository.add_group("romantic3", 1, "some desc")
            groups = group_repository.get_all()
            assert len(groups) == 3

    def test_delete_actor_by_id_bool(self):
        """Testing deleting actor by id"""
        with TestingSessionLocal() as db:
            group_repository = GroupRepository(db)
            group = group_repository.add_group("romantic1", 1, "some desc")
            assert group_repository.delete_group_by_id(group.id) is True

    def test_delete_actor_by_id_bool_false(self):
        """Testing deleting actor by id"""
        with TestingSessionLocal() as db:
            group_repository = GroupRepository(db)
            assert group_repository.delete_group_by_id(2) is False
