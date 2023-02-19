"""Module for Actor service layer."""
from app.actor.exceptions import ActorNotFound
from app.actor.repository import ActorRepository
from app.db import SessionLocal


class ActorService:
    """Class for Actor service layer ."""

    @staticmethod
    def add_actor(full_name, nationality):
        """
        The add_actor function adds a new actor to the database.
        It takes two parameters, full_name and nationality.
        The function returns the id of the newly added actor.
        """
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.add_actor(full_name, nationality)
        except Exception as err:
            raise err

    @staticmethod
    def get_all_actors():
        """
        The get_all_actors function returns all actors in the database.
        """
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.get_all_actors()
        except Exception as err:
            raise err

    @staticmethod
    def get_actor_by_id(actor_id: int):
        """
        The get_actor_by_id function is used to retrieve a single actor from the database by their ID.
        It takes in an integer as an argument and returns a dictionary containing the actor's information.
        """
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.get_actor_by_id(actor_id)
        except Exception as err:
            raise err

    @staticmethod
    def find_actor_by_name(name: str):
        """
        The find_actor_by_name function takes a name as an argument and returns the actor with that name.
        If no actor is found, it raises an exception.
        """
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.find_actor_by_name(name)
        except Exception as err:
            raise err

    @staticmethod
    def find_actor_by_last_name(last_name: str):
        """
        The find_actor_by_last_name function finds an actor by their last name.
        It takes a string as the parameter and returns an Actor object.
        """
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.find_actor_by_last_name(last_name)
        except Exception as err:
            raise err

    @staticmethod
    def change_actor_full_name(actor_id, full_name):
        """
        The change_actor_full_name function allows the user to change an actor's full name.
        It takes in two arguments, the actor_id and the new full name for that actor. It returns a dictionary
        with a key of 'success' and value of True or False depending on whether it was successful.
        """
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.change_actor_full_name(actor_id, full_name)
        except Exception as err:
            raise err

    @staticmethod
    def delete_actor_by_id(actor_id: int):
        """
        The delete_actor_by_id function deletes an actor from the database.
        It takes in a single parameter, which is the id of the actor to be deleted.
        If there is no actor with that id in the database, it raises an ActorNotFound exception.
        """
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                if actor_repository.delete_actor_by_id(actor_id) is None:
                    raise ActorNotFound(f'There is no actor with id {actor_id} in database.')
                return True
        except ActorNotFound as err:
            raise err
        except Exception as err:
            raise err
