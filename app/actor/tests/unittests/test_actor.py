import pytest
from sqlalchemy.exc import IntegrityError

from app.actor.exceptions import ActorNotFound
from app.actor.repository import ActorRepository
from app.tests import TestClass, TestingSessionLocal


class TestActorRepository(TestClass):

    def create_actors_for_methods(self):
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Robin Wright', 'American')
            actor = actor_repository.add_actor('Anthony Hopkins', 'American')

    def test_create_actor(self):
        """Test method add_actor."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Robin Wright', 'American')
            assert actor.full_name == 'Robin Wright'
            assert actor.nationality == 'American'

    def test_find_actor_by_name(self):
        """Test finding actor by name."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Rob W', 'American')
            actor = actor_repository.add_actor('Robin S', 'American')
            actor = actor_repository.add_actor('Robina M', 'American')
            actor = actor_repository.add_actor('Sofi Rob', 'American')
            actors = actor_repository.find_actor_by_name("rob")
            assert len(actors) == 3

    def test_find_actor_by_last_name(self):
        """Test finding actor by last name."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Rob Daniels', 'American')
            actor = actor_repository.add_actor('Dani Cruz', 'American')
            actor = actor_repository.add_actor('Rob Danish', 'American')
            actor = actor_repository.add_actor('Rob Smith', 'American')
            actors = actor_repository.find_actor_by_last_name("dani")
            assert len(actors) == 2

    def test_find_actor_by_full_name(self):
        """Test finding actor by name and last name."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Smith Rob', 'American')
            actor = actor_repository.add_actor('Rob Roby', 'American')
            actor = actor_repository.add_actor('Rob Smithy', 'American')
            actor = actor_repository.add_actor('Rob Smith', 'American')
            target_actors = actor_repository.find_actor_by_full_name("rob smith")
            assert len(target_actors) == 1

    def test_find_actor_by_full_name_error(self):
        """Test error finding actor by name and last name."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            with pytest.raises(ActorNotFound):
                actor_repository.find_actor_by_full_name("Rob Smith")

    def test_get_actor_by_id(self):
        """Test getting actor by id. """
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Rob Smith', 'American')
            test_actor = actor_repository.get_actor_by_id(actor.id)
            assert actor.id == test_actor.id

    def test_get_all_actors(self):
        """Test get all actors. """
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Rob Smith', 'American')
            actor = actor_repository.add_actor('Rob Smith', 'American')
            actor = actor_repository.add_actor('Rob Smith', 'American')
            actors = actor_repository.get_all_actors()
            assert len(actors) == 3

    def test_get_actor_by_id_error(self):
        """Test error finding actor by id."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            with pytest.raises(ActorNotFound):
                actor_repository.get_actor_by_id(3)

    def test_get_actor_full_name_by_id(self):
        """Test getting actor name and last name by id."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Rob Smith', 'American')
            full_name_tuple = actor_repository.get_actor_full_name_by_id(actor.id)
            assert actor.full_name == full_name_tuple[0]

    def test_get_actor_full_name_by_id_error(self):
        """Test error finding actor by id."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            with pytest.raises(ActorNotFound):
                actor_repository.get_actor_full_name_by_id(3)

    def test_change_actor_full_name(self):
        """Test changing actor's name and last name."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Rob Smith', 'American')
            actor_repository.change_actor_full_name(actor.id, "Smith Rob")
            assert actor.full_name == "Smith Rob"

    def test_change_actor_full_name_error(self):
        """Test error while changing actor's name and last name."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            with pytest.raises(ActorNotFound):
                actor_repository.change_actor_full_name("Rob Smith", 3)

    def delete_actor_by_id(self):
        """Testing deleting actor by id"""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Rob Smith', 'American')
            actor_repository.delete_actor_by_id(actor.id)
            assert actor_repository.get_actor_by_id(actor.id) is None

    def delete_actor_by_id_bool(self):
        """Testing deleting actor by id"""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Rob Smith', 'American')
            assert actor_repository.delete_actor_by_id(actor.id) is True

    def delete_actor_by_id_error(self):
        """Testing error when deleting actor by id"""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            with pytest.raises(ActorNotFound):
                actor_repository.delete_actor_by_id(3)
