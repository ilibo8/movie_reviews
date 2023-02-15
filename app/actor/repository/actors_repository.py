from typing import Type
from sqlalchemy.orm import Session
from app.actor.exceptions import ActorNotFound
from app.actor.model import Actor


class ActorRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_actor(self, full_name, nationality) -> Actor:
        actor = Actor(full_name, nationality)
        self.db.add(actor)
        self.db.commit()
        self.db.refresh(actor)
        return actor

    def get_all_actors(self) -> list[Type[Actor]]:
        actors = self.db.query(Actor).all()
        return actors

    def find_actor_by_name(self, name) -> list[Type[Actor]]:
        actor = self.db.query(Actor).filter(Actor.full_name.ilike(f'{name}%')).all()
        return actor

    def find_actor_by_last_name(self, last_name) -> list[Type[Actor]]:

        actor = self.db.query(Actor).filter(Actor.full_name.ilike(f'% {last_name}%')).all()
        return actor

    def find_actor_by_full_name(self, full_name) -> list[Actor]:
        actors = self.db.query(Actor).filter(Actor.full_name == full_name).all()
        if len(actors) == 0:
            raise ActorNotFound(f'There is no actor with that name and last name.')
        return actors

    def get_actor_by_id(self, id) -> Actor:

        actor = self.db.query(Actor).filter(Actor.id == id).first()
        if actor is None:
            raise ActorNotFound(f"There is no actor with id {id}.")
        return actor

    def get_actor_full_name_by_id(self, id) -> tuple:
        actor = self.db.query(Actor.full_name).filter(Actor.id == id).first()
        if actor is None:
            raise ActorNotFound(f"There is no actor with id {id}.")
        return actor

    def change_actor_full_name(self, actor_id, full_name) -> Actor:
        actor = self.db.query(Actor).filter(Actor.id == actor_id).first()
        if actor is None:
            raise ActorNotFound(f'There is no actor with id {actor_id} in database.')
        actor.full_name = full_name
        self.db.add(actor)
        self.db.commit()
        self.db.refresh(actor)
        return actor

    def delete_actor_by_id(self, actor_id: int) -> bool:
        actor = self.db.query(Actor).filter(Actor.id == actor_id).first()
        if actor is None:
            raise ActorNotFound(f"No actor with id {actor_id}.")
        self.db.delete(actor)
        self.db.commit()
        return True

