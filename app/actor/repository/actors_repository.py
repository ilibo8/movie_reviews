"""Module for Actor Repository"""
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.actor.exceptions import ActorNotFound
from app.actor.model import Actor


class ActorRepository:
    """Class for Actor repository layer."""
    def __init__(self, db: Session):
        self.db = db

    def add_actor(self, full_name: str, nationality: str) -> Actor:
        """
        The add_actor function adds a new actor to the database.
        It takes two parameters, full_name and nationality.
        If an actor with that name already exists in the database, it raises a DuplicateEntry exception.
        """
        try:
            actor = Actor(full_name, nationality)
            self.db.add(actor)
            self.db.commit()
            self.db.refresh(actor)
            return actor
        except IntegrityError as err:
            raise IntegrityError from err

    def get_all_actors(self) -> list[Actor]:
        """
        The get_all_actors function returns a list of all the actors in the database.
        """
        actors = self.db.query(Actor).all()
        return actors

    def find_actor_by_name(self, name) -> list[Actor]:
        """
        The find_actor_by_name function takes in a string and returns a list of actors whose name contains
        the inputted string.
        """
        actor = self.db.query(Actor).filter(Actor.full_name.ilike(f'{name}%')).all()
        return actor

    def find_actor_by_last_name(self, last_name) -> list[Actor]:
        """
        The find_actor_by_last_name function takes a last name as an argument and returns a list of actors whose
        last names contain the string provided by the user.
        """
        actor = self.db.query(Actor).filter(Actor.full_name.ilike(f'% {last_name}%')).all()
        return actor

    def get_actor_by_full_name(self, full_name) -> Actor:
        """
        The function takes a full name and returns an actor object.
        """
        return self.db.query(Actor).filter(Actor.full_name == full_name).first()

    def get_actor_by_id(self, actor_id) -> Actor:
        """
        The get_actor_by_id function takes an id as a parameter and returns the actor with that id.
        If no actor is found with that id, it raises an ActorNotFound exception.
        """
        actor = self.db.query(Actor).filter(Actor.id == actor_id).first()
        if actor is None:
            raise ActorNotFound(f"There is no actor with id {actor_id}.")
        return actor

    def get_actor_full_name_by_id(self, actor_id) -> str:
        """
        The get_actor_full_name_by_id function takes an actor id as a parameter and returns the full name of the actor.
        If there is no actor with that id, it raises an ActorNotFound exception.
        """
        actor = self.db.query(Actor.full_name).filter(Actor.id == actor_id).first()
        if actor is None:
            raise ActorNotFound(f"There is no actor with id {actor_id}.")
        return actor[0]

    def change_actor_full_name(self, actor_id, full_name) -> Actor:
        """
        The change_actor_full_name function changes the full name of an actor.
        It takes two arguments: actor_id and full_name. It returns an Actor object with the updated information.
        """
        actor = self.db.query(Actor).filter(Actor.id == actor_id).first()
        if actor is None:
            raise ActorNotFound(f'There is no actor with id {actor_id} in database.')
        actor.full_name = full_name
        self.db.add(actor)
        self.db.commit()
        self.db.refresh(actor)
        return actor

    def delete_actor_by_id(self, actor_id: int) -> bool:
        """
        The delete_actor_by_id function deletes an actor from the database.
        It takes in a single parameter, actor_id, which is the id of the actor to be deleted.
        If no such actor exists in the database, it raises an exception.
        """
        actor = self.db.query(Actor).filter(Actor.id == actor_id).first()
        if actor is None:
            raise ActorNotFound(f"No actor with id {actor_id}.")
        self.db.delete(actor)
        self.db.commit()
        return True
