from app.actor.exceptions import ActorNotFoundException
from app.actor.service import ActorService
from fastapi import HTTPException, Response


class ActorController:

    @staticmethod
    def add_actor(full_name, nationality):
        try:
            return ActorService.add_actor(full_name, nationality)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_actors():
        try:
            return ActorService.get_all_actors()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def find_actor_by_name(name: str):
        try:
            return ActorService.find_actor_by_name(name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def find_actor_by_last_name(last_name: str):
        try:
            return ActorService.find_actor_by_last_name(last_name)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def find_actor_by_id(id: int):
        try:
            return ActorService.find_actor_by_id(id)
        except ActorNotFoundException as e:
            raise HTTPException(status_code=400, detail=str(e.message))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def change_actor_full_name(actor_id, full_name):
        try:
            return ActorService.change_actor_full_name(actor_id, full_name)
        except ActorNotFoundException as e:
            raise HTTPException(status_code=400, detail=str(e.message))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def change_actor_nationality(actor_id, nationality):
        try:
            return ActorService.change_actor_nationality(actor_id, nationality)
        except ActorNotFoundException as e:
            raise HTTPException(status_code=400, detail=str(e.message))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_actor_by_id(actor_id: int):
        try:
            if ActorService.delete_actor_by_id(actor_id):
                return Response(content=f"Actor with id - {actor_id} is deleted", status_code=200)
        except ActorNotFoundException as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
