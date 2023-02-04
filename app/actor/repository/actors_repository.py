from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.actor.exceptions import ActorNotFoundException
from app.actor.model import Actor


class ActorRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_actor(self, full_name, nationality):
        try:
            actor = Actor(full_name, nationality)
            self.db.add(actor)
            self.db.commit()
            self.db.refresh(actor)
            return actor
        except Exception as e:
            raise e

    def get_all_actors(self):
        try:
            actors = self.db.query(Actor).all()
            return actors
        except Exception as e:
            raise e

    def find_actor_by_name(self, name):
        try:
            actor = self.db.query(Actor).filter(Actor.full_name.ilike(f'{name}%')).all()
            return actor
        except Exception as e:
            raise e

    def find_actor_by_last_name(self, last_name):
        try:
            actor = self.db.query(Actor).filter(Actor.full_name.ilike(f'% {last_name}%')).all()
            return actor
        except Exception as e:
            raise e

    def find_actor_by_full_name(self, full_name):
        try:
            actor = self.db.query(Actor).filter(Actor.full_name == full_name).all()
            if actor is None:
                raise ActorNotFoundException(f'That actor is not in database.')
            return actor
        except Exception as e:
            raise e

    def find_actor_by_id(self, id):
        try:
            actor = self.db.query(Actor).filter(Actor.id == id).first()
            if actor is None:
                raise ActorNotFoundException(f"There is no actor with id {id}.")
            return actor
        except Exception as e:
            raise e

    def change_actor_full_name(self, actor_id, full_name):
        try:
            actor = self.db.query(Actor).filter(Actor.id == actor_id).first()
            if actor is None:
                raise ActorNotFoundException(f'There is no actor with id {actor_id} in database.')
            actor.full_name = full_name
            self.db.add(actor)
            self.db.commit()
            self.db.refresh(actor)
            return actor
        except Exception as e:
            raise e

    def change_actor_nationality(self, actor_id, nationality):
        try:
            actor = self.db.query(Actor).filter(Actor.id == actor_id).first()
            if actor is None:
                raise ActorNotFoundException(f'There is no actor with id {actor_id} in database.')
            actor.nationality = nationality
            self.db.add(actor)
            self.db.commit()
            self.db.refresh(actor)
            return actor
        except Exception as e:
            raise e

    def delete_actor_by_id(self, actor_id: int):
        try:
            actor = self.db.query(Actor).filter(Actor.id == actor_id).first()
            if actor is None:
                raise ActorNotFoundException(f'There is no actor with id {actor_id} in database.')
            self.db.delete(actor)
            self.db.commit()
            return True
        except Exception as e:
            raise e
