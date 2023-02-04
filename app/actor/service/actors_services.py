from app.actor.exceptions import ActorNotFoundException
from app.actor.repository import ActorRepository
from app.db.database import SessionLocal


class ActorService:

    @staticmethod
    def add_actor(full_name, nationality):
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.add_actor(full_name, nationality)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_actors():
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.get_all_actors()
        except Exception as e:
            raise e

    @staticmethod
    def find_actor_by_name(name: str):
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.find_actor_by_name(name)
        except Exception as e:
            raise e

    @staticmethod
    def find_actor_by_last_name(last_name: str):
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.find_actor_by_last_name(last_name)
        except Exception as e:
            raise e

    @staticmethod
    def find_actor_by_id(id: int):
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.find_actor_by_id(id)
        except Exception as e:
            raise e

    @staticmethod
    def change_actor_full_name(actor_id, full_name):
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.change_actor_full_name(actor_id, full_name)
        except Exception as e:
            raise e

    @staticmethod
    def change_actor_nationality(actor_id, nationality):
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                return actor_repository.change_actor_nationality(actor_id, nationality)
        except Exception as e:
            raise e

    @staticmethod
    def delete_actor_by_id(actor_id: int):
        try:
            with SessionLocal() as db:
                actor_repository = ActorRepository(db)
                if actor_repository.delete_actor_by_id(actor_id) is None:
                    raise ActorNotFoundException(f'There is no actor with id {actor_id} in database.')
                return True
        except Exception as e:
            raise e
