import pytest
from sqlalchemy.exc import IntegrityError

from app.movie.repository import MovieRepository
from app.tests import TestClass, TestingSessionLocal


class TestMovieRepository(TestClass):

    def test_add_movie(self):
        """Test method add_movie."""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie = movie_repository.add_movie("title", "director", 1999, "country")
            assert movie.title == "title"
            assert movie.director == "director"
            assert movie.release_year == 1999
            assert movie.country_of_origin == "country"

    def test_add_movie_error(self):
        """Test method add_movie integrity error."""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title", "director", 1999, "country")
            with pytest.raises(IntegrityError):
                movie_repository.add_movie("title", "director", 1999, "country")

    def test_get_all_movies(self):
        """Test get all movies. """
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title1", "director", 1999, "country")
            movie_repository.add_movie("title2", "director", 1999, "country")
            movie_repository.add_movie("title3", "director", 1999, "country")
            movies = movie_repository.get_all_movies()
            assert len(movies) == 3

    ### get movie by id

    def test_get_movie_id_by_title(self):
        """Test method for getting movie id from movie title"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title1", "director", 1999, "country")
            movie_repository.add_movie("title2", "director", 1999, "country")
            movie_repository.add_movie("title3", "director", 1999, "country")
            assert movie_repository.get_movie_id_by_title("TITLE3") == 3
            assert movie_repository.get_movie_id_by_title("titLe2") == 2
