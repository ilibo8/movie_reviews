"""Module for testing MovieGenre repository"""
import pytest

from app.genre.repository import GenreRepository
from app.movie.exceptions import DuplicateDataEntry, MovieGenreNotFound
from app.movie.repository import MovieRepository, MovieGenreRepository
from app.tests import TestClass, TestingSessionLocal


class TestMovieGenreRepository(TestClass):
    """Class for testing methods for MovieGenre repository"""

    def create_foreign_keys(self):
        """Create data for foreign keys to use in test methods"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            genre_repository = GenreRepository(db)
            movie_repository.add_movie("movie1", "d1", 2001, "c1")
            movie_repository.add_movie("movie2", "d2", 2002, "c2")
            movie_repository.add_movie("movie3", "d3", 2003, "c3")
            genre_repository.add_genre("a")
            genre_repository.add_genre("b")
            genre_repository.add_genre("c")

    def test_add_movie_genre(self):
        """Test method add_movie_genre."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            movie_genre_repo = MovieGenreRepository(db)
            new = movie_genre_repo.add_movie_genre(movie_id=1, genre_name="a")
            assert new.genre_name == "a"

    def test_add_movie_genre_error(self):
        """Test error for method add_movie_genre."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            movie_genre_repo = MovieGenreRepository(db)
            movie_genre_repo.add_movie_genre(1, "a")
            with pytest.raises(DuplicateDataEntry):
                movie_genre_repo.add_movie_genre(1, "a")

    def test_get_all(self):
        """Test method get all. """
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            movie_genre_repo = MovieGenreRepository(db)
            movie_genre_repo.add_movie_genre(1, "a")
            movie_genre_repo.add_movie_genre(1, "b")
            movie_genre_repo.add_movie_genre(2, "a")
            assert len(movie_genre_repo.get_all()) == 3

    def test_get_all_movie_ids_of_certain_genre(self):
        """Test method get_all_movie_ids_of_certain_genre. """
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            movie_genre_repo = MovieGenreRepository(db)
            movie_genre_repo.add_movie_genre(1, "a")
            movie_genre_repo.add_movie_genre(1, "b")
            movie_genre_repo.add_movie_genre(2, "a")
            assert movie_genre_repo.get_all_movie_ids_of_certain_genre("a") == [1, 2]


    def test_delete_movie_genre(self):
        """Test method delete movie genre"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            movie_genre_repo = MovieGenreRepository(db)
            movie_genre_repo.add_movie_genre(1, "a")
            assert movie_genre_repo.delete_movie_genre(1, "a") is True

    def test_delete_movie_genre_error(self):
        """Test raising error for method delete_movie_genre"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            movie_genre_repo = MovieGenreRepository(db)
            with pytest.raises(MovieGenreNotFound):
                movie_genre_repo.delete_movie_genre(1, "a")
