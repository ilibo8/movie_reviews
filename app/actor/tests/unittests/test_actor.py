"""Module for testing Actor repository."""
import pytest
from app.actor.exceptions import ActorNotFound, DuplicateEntry
from app.actor.repository import ActorRepository
from app.tests import TestClass, TestingSessionLocal


class TestActorRepository(TestClass):

    def test_create_actor(self):
        """Test method add_actor."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Robin Wright', 'American')
            assert actor.full_name == 'Robin Wright'
            assert actor.nationality == 'American'

    def test_create_actor_error(self):
        """Test method add_actor error."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor_repository.add_actor('Robin Wright', 'American')
            with pytest.raises(DuplicateEntry):
                actor_repository.add_actor('Robin Wright', 'American')

    def test_find_actor_by_name(self):
        """Test finding actor by name."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor_repository.add_actor('Rob W', 'American')
            actor_repository.add_actor('Robin S', 'American')
            actor_repository.add_actor('Robina M', 'American')
            actor_repository.add_actor('Sofi Rob', 'American')
            actors = actor_repository.find_actor_by_name("rob")
            assert len(actors) == 3

    def test_find_actor_by_last_name(self):
        """Test finding actor by last name."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor_repository.add_actor('Rob Daniels', 'American')
            actor_repository.add_actor('Dani Cruz', 'American')
            actor_repository.add_actor('Rob Danish', 'American')
            actor_repository.add_actor('Rob Smith', 'American')
            actors = actor_repository.find_actor_by_last_name("dani")
            assert len(actors) == 2

    def test_find_actor_by_full_name_error(self):
        """Test error finding actor by name and last name."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            with pytest.raises(ActorNotFound):
                actor_repository.get_actor_by_full_name("Rob Smith")

    def test_get_all_actors(self):
        """Test get all actors. """
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor_repository.add_actor('Rob Smith', 'American')
            actor_repository.add_actor('Roby Smith', 'American')
            actor_repository.add_actor('Rob Smithy', 'American')
            actors = actor_repository.get_all_actors()
            assert len(actors) == 3

    def test_get_actor_by_id(self):
        """Test finding actor by id."""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor_repository.add_actor('Roby Smith', 'American')
            actor_repository.add_actor('Rob Smithy', 'American')
            actor1 = actor_repository.get_actor_by_id(1)
            actor2 = actor_repository.get_actor_by_id(2)
            assert actor1.full_name == 'Roby Smith'
            assert actor2.full_name == 'Rob Smithy'

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
            assert actor.full_name == full_name_tuple

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

    def test_delete_actor_by_id(self):
        """Testing deleting actor by id"""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Rob Smith', 'American')
            assert actor_repository.delete_actor_by_id(actor.id) is True

    def test_delete_actor_by_id_bool(self):
        """Testing deleting actor by id"""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            actor = actor_repository.add_actor('Rob Smith', 'American')
            assert actor_repository.delete_actor_by_id(actor.id) is not False

    def test_delete_actor_by_id_error(self):
        """Testing error when deleting actor by id"""
        with TestingSessionLocal() as db:
            actor_repository = ActorRepository(db)
            with pytest.raises(ActorNotFound):
                actor_repository.delete_actor_by_id(3)
