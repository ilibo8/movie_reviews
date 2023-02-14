import pytest
from app.tests import TestClass, TestingSessionLocal
from app.users.exceptions import AlreadyExist, UserNotFound
from app.users.repository import UserRepository


class TestUserRepo(TestClass):

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

    def test_change_group_ownership(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user = user_repository.create_user("rob", "rob123", "r@gmail.com")
            user = user_repository.change_group_ownership(user.user_name, True)
            assert user.is_group_owner is True

    def test_change_group_ownership2(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            user = user_repository.create_user("rob", "rob123", "r@gmail.com")
            user = user_repository.change_group_ownership(user.user_name, True)
            user = user_repository.change_group_ownership(user.user_name, False)
            assert user.is_group_owner is not True

    def test_change_group_ownership_error(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            with pytest.raises(UserNotFound):
                user_repository.change_group_ownership("bob", True)

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
            assert user_repository.delete_user_by_id("something") is not True

