"""Module for testing genre repository"""
import pytest
from sqlalchemy.exc import IntegrityError
from app.genre.exceptions import GenreNotFound
from app.genre.repository import GenreRepository
from app.tests import TestClass, TestingSessionLocal


class TestGenreRepository(TestClass):
    """Class for testing genre repository methods."""

    def test_add_genre(self):
        """Test method add_genre."""
        with TestingSessionLocal() as dbs:
            genre_repository = GenreRepository(dbs)
            genre = genre_repository.add_genre("drama")
            assert genre.name == "drama"

    def test_add_genre_error(self):
        """Test method add_genre."""
        with TestingSessionLocal() as dbs:
            genre_repository = GenreRepository(dbs)
            genre_repository.add_genre("drama")
            with pytest.raises(IntegrityError):
                genre_repository.add_genre("drama")

    def test_get_all_genre(self):
        """Test get all genres. """
        with TestingSessionLocal() as dbs:
            genre_repository = GenreRepository(dbs)
            genre_repository.add_genre("drama")
            genre_repository.add_genre("comedy")
            genre_repository.add_genre("horror")
            genres = genre_repository.get_all_genres()
            assert len(genres) == 3

    def test_delete(self):
        """Test delete genre by name"""
        with TestingSessionLocal() as dbs:
            genre_repository = GenreRepository(dbs)
            genre_repository.add_genre("drama")
            genre_repository.add_genre("comedy")
            genre_repository.add_genre("horror")
            genre_repository.delete("drama")
            genres = genre_repository.get_all_genres()
            assert len(genres) == 2

    def test_delete2(self):
        """Test delete genre by name"""
        with TestingSessionLocal() as dbs:
            genre_repository = GenreRepository(dbs)
            genre_repository.add_genre("drama")
            assert genre_repository.delete("drama") is True

    def test_delete_error(self):
        """Test raising GenreNotFound."""
        with TestingSessionLocal() as dbs:
            genre_repository = GenreRepository(dbs)
            with pytest.raises(GenreNotFound):
                genre_repository.delete("some")

    def test_check_is_there(self):
        """Test method check is there."""
        with TestingSessionLocal() as dbs:
            genre_repository = GenreRepository(dbs)
            genre_repository.add_genre("drama")
            assert genre_repository.check_is_there("drama") is True

    def test_check_is_there2(self):
        """Test method check is there."""
        with TestingSessionLocal() as dbs:
            genre_repository = GenreRepository(dbs)
            genre_repository.add_genre("drama")
            assert genre_repository.check_is_there("comedy") is False
