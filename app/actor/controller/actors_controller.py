"""Module for Actor Controller."""
from fastapi import HTTPException, Response
from app.actor.exceptions import ActorNotFound, DuplicateEntry
from app.actor.service import ActorService


class ActorController:
    """Class for Actor controller layer."""

    @staticmethod
    def add_actor(full_name, nationality):
        """
        The add_actor function adds an actor to the database.
        It takes two arguments, full_name and nationality.
        It returns a dictionary with the key 'actor' and value of the newly created actor's id.

        :param full_name: Store the name of the actor being added to the database
        :param nationality: Determine the nationality of the actor
        :return: A dictionary with the actor's information
        """
        try:
            return ActorService.add_actor(full_name, nationality)
        except DuplicateEntry as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all_actors():
        """
        The get_all_actors function returns all actors in the database.

        :return: A list of actors
        """
        try:
            return ActorService.get_all_actors()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all_actors_names():
        """
        The get_all_actors_names function returns a list of all the actors' names in the database.
        It does this by querying the Actor table and returning a list of all actor names.

        :return: A list of all the actors names in alphabetical order
        """
        try:
            actor_names = []
            actors = ActorService.get_all_actors()
            for actor in actors:
                actor_names.append(actor.full_name)
            actor_names.sort()
            return actor_names
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def find_actor_by_name(name: str):
        """
        The find_actor_by_name function finds an actor by their name.
        It returns the actor if found, otherwise it returns None.

        :param name:str: Search for a specific actor by name
        :return: A single actor object
        """

        try:
            return ActorService.find_actor_by_name(name)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def find_actor_by_last_name(last_name: str):
        """
        The find_actor_by_last_name function finds an actor by their last name.
        It returns the actor if found, otherwise it returns a 404 error.

        :param last_name:str: Specify the last name of the actor to be searched for
        :return: A dictionary with the actor's information
        """
        try:
            return ActorService.find_actor_by_last_name(last_name)
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err)) from err

    @staticmethod
    def get_actor_by_id(actor_id: int):
        """
        The get_actor_by_id function is used to retrieve a single actor from the database by their unique id.
        It takes in an integer as an argument, and returns a dictionary containing the information of that actor.

        :param actor_id:int: Specify the actor_id of the actor to be returned
        :return: The actor with the given id
        """

        try:
            return ActorService.get_actor_by_id(actor_id)
        except ActorNotFound as err:
            raise HTTPException(status_code=400, detail=str(err.message)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def change_actor_full_name(actor_id, full_name):
        """
        The change_actor_full_name function is used to change the full name of an actor.
        It takes in two parameters, actor_id and full_name. It then calls the ActorService class's
        change_actor_full_name function which returns a dictionary with a key of ; and value True or False.
        If it was successful, it returns True otherwise it will return False.

        :param actor_id: Identify the actor to be modified
        :param full_name: Change the full name of an actor
        :return: The actor id of the actor that was changed
        """

        try:
            return ActorService.change_actor_full_name(actor_id, full_name)
        except ActorNotFound as err:
            raise HTTPException(status_code=400, detail=str(err.message)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def delete_actor_by_id(actor_id: int):
        """
        The delete_actor_by_id function deletes an actor from the database by their id.
        It takes in a parameter of type int, which is the id of the actor to be deleted.
        If no such actor exists, it raises an ActorNotFound exception.

        :param actor_id:int: Identify the actor to be deleted
        :return: A response object
        """

        try:
            if ActorService.delete_actor_by_id(actor_id):
                return Response(content=f"Actor with id - {actor_id} is deleted", status_code=200)
        except ActorNotFound as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
