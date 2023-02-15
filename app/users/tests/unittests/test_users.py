"""Module for testing user repository"""
import pytest
from app.tests import TestClass, TestingSessionLocal
from app.users.exceptions import AlreadyExist, UserNotFound
from app.users.repository import UserRepository


class TestUserRepository(TestClass):
    """Class for testing User repository"""

    def test_create_user(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user = user_repository.create_user("rob", "rob123", "r@gmail.com")
            assert user.email == "r@gmail.com"
            assert user.user_name == "rob"
            assert user.is_superuser is False
            assert user.is_group_owner is False

    def test_create_user_error_user_name(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user_repository.create_user("rob", "rob123", "r@gmail.com")
            with pytest.raises(AlreadyExist):
                user_repository.create_user("rob", "rob123", "rb@gmail.com")

    def test_create_user_error_email(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user_repository.create_user("rob", "rob123", "r@gmail.com")
            with pytest.raises(AlreadyExist):
                user_repository.create_user("roby", "rob123", "r@gmail.com")

    def test_create_super_user(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            super_user = user_repository.create_super_user("rob", "rob123", "r@gmail.com")
            assert super_user.user_name == "rob"
            assert super_user.email == "r@gmail.com"
            assert super_user.is_superuser is True
            assert super_user.is_group_owner is False

    def test_create_super_user_error_user_name(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user_repository.create_user("rob", "rob123", "r@gmail.com")
            with pytest.raises(AlreadyExist):
                user_repository.create_user("rob", "rob123", "rb@gmail.com")

    def test_create_super_user_error_email(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user_repository.create_user("rob", "rob123", "r@gmail.com")
            with pytest.raises(AlreadyExist):
                user_repository.create_user("roby", "rob123", "r@gmail.com")

    def test_get_user_by_id(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user = user_repository.create_user("rob", "rob123", "r@gmail.com")
            user2 = user_repository.get_user_by_id(user.id)
            assert user == user2 ###!!!!!!

    def test_get_user_name_by_id(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user_repository.create_user("rob", "rob123", "r@gmail.com")
            assert user_repository.get_user_name_by_user_id(1) == "rob"

    def test_get_user_by_user_name(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user = user_repository.create_user("rob", "rob123", "r@gmail.com")
            user2 = user_repository.get_user_by_user_name(user.user_name)
            assert user == user2

    def test_get_user_by_user_name_error(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            with pytest.raises(UserNotFound):
                user_repository.get_user_by_user_name("bob")


    def test_get_all_users(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user_repository.create_user("rob1", "rob123", "r1@gmail.com")
            user_repository.create_user("rob2", "rob123", "r2@gmail.com")
            user_repository.create_user("rob3", "rob123", "r3@gmail.com")
            user_repository.create_user("rob4", "rob123", "r4@gmail.com")
            all_users = user_repository.get_all_users()
            assert len(all_users) == 4

    def test_delete_user_by_id(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user = user_repository.create_user("rob", "rob123", "r@gmail.com")
            assert user_repository.delete_user_by_id(user.id) is not False

    def test_delete_user_by_id_error(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            assert user_repository.delete_user_by_id(1) is not True
