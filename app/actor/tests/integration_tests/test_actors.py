"""Module for testing Actor routes"""
from http import HTTPStatus
from app.tests import TestClass, client
from app.users.service import UserService


class TestActorRoutes(TestClass):
    """Class for testing Actro routes"""
    def setup_super_user(self):
        """
        Create super_user to get token.
        """
        UserService.create_super_user("user", "password", "user@gmail.com")
        response = client.post(url="/api/login", json={"user_name": "user", "password": "password",
                                                       "email": "user@gmail.com"})
        token = response.json()["access_token"]
        return token

    def test_add_actor(self):
        """
        The test_add_actor function tests the add_actor endpoint.
        """
        token = self.setup_super_user()

        response = client.post(
            url="/api/superuser/movies/actors/add-actor",
            json={"full_name": "John Doe", "nationality": "American"},
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.OK
        actor = response.json()
        assert actor["full_name"] == "John Doe"
        assert actor["nationality"] == "American"

    def test_get_all_actors(self):
        """
        This function tests the get_all_school_years endpoint
        """
        token = self.setup_super_user()
        client.post(url="/api/superuser/movies/actors/add-actor",
                    json={"full_name": "John Doe",
                          "nationality": "American"},
                    headers={"Authorization": f"Bearer {token}"})
        client.post(url="/api/superuser/movies/actors/add-actor",
                    json={"full_name": "John Smith",
                          "nationality": "American"},
                    headers={"Authorization": f"Bearer {token}"})
        response = client.get(url="/api/superuser/movies/actors/get-all",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        output = response.json()
        assert len(output) == 2
        assert output[0]["full_name"] == "John Doe"
        assert output[0]["nationality"] == "American"
        assert output[1]["full_name"] == "John Smith"
        assert output[1]["nationality"] == "American"
