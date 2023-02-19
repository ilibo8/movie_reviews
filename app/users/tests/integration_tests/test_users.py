from app.tests import TestClass, client, TestingSessionLocal
from app.users.model import User
from app.users.service import UserService


class TestUserRoutes(TestClass):

    def setup_super_user(self):
        UserService.create_super_user("mihajlo@gmail.com", "sifra")

        response = client.post(url="/api/users/login", json={"email": "mihajlo@gmail.com", "password": "sifra"})
        token = response.json()["access_token"]
        return token

    def create_user(self):
        user = UserService.create_user("ivantot@gmail.com", "dgfdhy")
        return user

    # def test_create_route(self):
    #     response = client.post(url="/api/users/add-new-user",
    #                            json={"email": "mihajlo12389@gmail.com", "password": "sifra"})
    #     assert response.status_code == 200
    #     assert response.json()["email"] == "mihajlo12389@gmail.com"

    def test_create_super_user(self):
        token = self.setup_super_user()

        response = client.post(url="/api/users/add-new-super-user",
                               json={"email": "mihajlo123123@gmail.com", "password": "sifra"},
                               headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        user = response.json()
        assert user["email"] == "mihajlo123123@gmail.com"
        assert user["is_superuser"] is True

    def test_get_all_users(self):
        token = self.setup_super_user()
        response = client.get(url="/api/users/get-all-users",
                              headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 1

    def test_update_user(self):
        user = self.create_user()
        assert isinstance(user, User)

        response = client.put(url=f"/api/users/update/is_active?user_id={user.id}&is_active=False")

        assert response.status_code == 200
