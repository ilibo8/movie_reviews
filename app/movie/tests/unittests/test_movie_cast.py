"""Module for testing MovieGenre repository"""
import pytest

from app.actor.repository import ActorRepository
from app.movie.exceptions import DuplicateDataEntry, MovieNotFound, MovieCastNotFound
from app.movie.repository import MovieRepository, MovieCastRepository
from app.tests import TestClass, TestingSessionLocal


class TestMovieCastRepository(TestClass):
    """Class for testing MovieCast repository"""

    def create_foreign_keys(self):
        with TestingSessionLocal() as dbs:
            movie_repository = MovieRepository(dbs)
            actor_repository = ActorRepository(dbs)
            movie_repository.add_movie("movie1", "d1", 2001, "c1")
            movie_repository.add_movie("movie2", "d2", 2002, "c2")
            movie_repository.add_movie("movie3", "d3", 2003, "c3")
            actor_repository.add_actor("actor1", "a")
            actor_repository.add_actor("actor2", "a")
            actor_repository.add_actor("actor3", "a")

    def test_add(self):
        """Test method add."""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            movie_cast_repo = MovieCastRepository(dbs)
            member = movie_cast_repo.add(1, 2)
            assert member.actor_id == 2

    def test_add_err(self):
        """Test raising error for method add."""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            movie_cast_repo = MovieCastRepository(dbs)
            movie_cast_repo.add(1, 2)
            with pytest.raises(DuplicateDataEntry):
                movie_cast_repo.add(1, 2)

    def test_get_all(self):
        """Test method get all. """
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            movie_cast_repo = MovieCastRepository(dbs)
            movie_cast_repo.add(1, 1)
            movie_cast_repo.add(1, 2)
            movie_cast_repo.add(1, 3)
            assert len(movie_cast_repo.get_all()) == 3

    def test_get_cast_ids_by_movie_id(self):
        """Test method get_cast_ids_by_movie_id"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            movie_cast_repo = MovieCastRepository(dbs)
            movie_cast_repo.add(1, 1)
            movie_cast_repo.add(1, 2)
            movie_cast_repo.add(1, 3)
            assert movie_cast_repo.get_cast_ids_by_movie_id(1) == [1, 2, 3]

    def test_get_cast_ids_by_movie_id_error(self):
        """Test raising error for method get_cast_ids_by_movie_id."""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            movie_cast_repo = MovieCastRepository(dbs)
            with pytest.raises(MovieNotFound):
                movie_cast_repo.get_cast_ids_by_movie_id(4)

    def test_get_movie_ids_by_actor_id(self):
        """Test method get_movie_ids_by_actor_id"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            movie_cast_repo = MovieCastRepository(dbs)
            movie_cast_repo.add(1, 1)
            movie_cast_repo.add(1, 2)
            movie_cast_repo.add(1, 3)
            movie_cast_repo.add(2, 3)
            assert movie_cast_repo.get_movie_ids_by_actor_id(3) == [1, 2]

    def test_get_movie_ids_by_actor_id_error(self):
        """Test raising error for method get_movie_ids_by_actor_id."""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            movie_cast_repo = MovieCastRepository(dbs)
            with pytest.raises(MovieNotFound):
                movie_cast_repo.get_movie_ids_by_actor_id(4)

    def test_delete_movie_cast(self):
        """Test method delete_movie_cast"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            movie_cast_repo = MovieCastRepository(dbs)
            movie_cast_repo.add(1, 3)
            assert movie_cast_repo.delete_movie_cast(1, 3) is True

    def test_delete_movie_cast_error(self):
        """Test raising MovieCastNotFound."""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            movie_cast_repo = MovieCastRepository(dbs)
            with pytest.raises(MovieCastNotFound):
                movie_cast_repo.delete_movie_cast(1, 3)
