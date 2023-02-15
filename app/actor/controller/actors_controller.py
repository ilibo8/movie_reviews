"""Module for Actor Controller."""
from fastapi import HTTPException, Response
from sqlalchemy.exc import IntegrityError
from app.actor.exceptions import ActorNotFound
from app.actor.service import ActorService



class ActorController:
    """Controller layer for Actor"""

    @staticmethod
    def add_actor(full_name, nationality):
        """Method for adding actor to database."""
        try:
            return ActorService.add_actor(full_name, nationality)
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all_actors():
        """Method for getting list of all actors."""
        try:
            return ActorService.get_all_actors()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all_actors_names():
        """Method for getting list of all actor's names in database."""
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
        """Method for finding actor by name."""
        try:
            return ActorService.find_actor_by_name(name)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def find_actor_by_last_name(last_name: str):
        """Method for finding actor by last name."""
        try:
            return ActorService.find_actor_by_last_name(last_name)
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err)) from err

    @staticmethod
    def find_actor_by_full_name(full_name: str):
        """Method for finding actor by name and last name."""
        try:
            return ActorService.find_actor_by_full_name(full_name)
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err)) from err

    @staticmethod
    def get_actor_by_id(actor_id: int):
        """Method for getting actor by id."""
        try:
            return ActorService.get_actor_by_id(actor_id)
        except ActorNotFound as err:
            raise HTTPException(status_code=400, detail=str(err.message)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def change_actor_full_name(actor_id, full_name):
        """Method for changing actor name and last name."""
        try:
            return ActorService.change_actor_full_name(actor_id, full_name)
        except ActorNotFound as err:
            raise HTTPException(status_code=400, detail=str(err.message)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def delete_actor_by_id(actor_id: int):
        """Method for deleting actor by id."""
        try:
            if ActorService.delete_actor_by_id(actor_id):
                return Response(content=f"Actor with id - {actor_id} is deleted", status_code=200)
        except ActorNotFound as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
