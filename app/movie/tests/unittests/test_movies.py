"""Module for testing Movie repository"""
import pytest
from sqlalchemy.exc import IntegrityError
from app.movie.exceptions import MovieNotFound
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

    def test_get_all_movies_order_by_name(self):
        """Test get all movies. """
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("c", "director", 1999, "country")
            movie_repository.add_movie("a", "director", 1999, "country")
            movie_repository.add_movie("b", "director", 1999, "country")
            movies = movie_repository.get_all_movies_order_by_name()
            assert len(movies) == 3
            assert movies[0].title == "a"
            assert movies[1].title == "b"
            assert movies[2].title == "c"

    def test_get_movie_by_id(self):
        """Test method get_movie_by_id."""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title", "director", 1999, "country")
            assert movie_repository.get_movie_by_id(1).title == "title"
            assert movie_repository.get_movie_by_id(1).release_year == 1999

    def test_get_movie_by_title(self):
        """Test method get_movie_by_title."""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("red", "director", 1999, "country")
            movie_repository.add_movie("blue", "director", 2000, "country")
            movie_repository.add_movie("yellow", "director", 2001, "country")
            assert movie_repository.get_movie_by_title("red").release_year == 1999
            assert movie_repository.get_movie_by_title("blue").release_year == 2000
            assert movie_repository.get_movie_by_title("yellow").id == 3

    def test_get_title_by_id(self):
        """Test method for get movie title by its id"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title1", "director", 1999, "country")
            movie_repository.add_movie("title2", "director", 1999, "country")
            assert movie_repository.get_title_by_id(1) == "title1"
            assert movie_repository.get_title_by_id(2) == "title2"

    def test_get_movie_id_by_title(self):
        """Test method for getting movie id from movie title"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title1", "director", 1999, "country")
            movie_repository.add_movie("title2", "director", 1999, "country")
            movie_repository.add_movie("title3", "director", 1999, "country")
            assert movie_repository.get_movie_id_by_title("TITLE3") == 3
            assert movie_repository.get_movie_id_by_title("titLe2") == 2

    def test_get_movie_id_by_title_error(self):
        """Test raising error for method getting movie id from movie title"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            with pytest.raises(MovieNotFound):
                movie_repository.get_movie_id_by_title("something")

    def test_get_movies_by_word_in_title(self):
        """Test method for getting movies by word in movie title"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("Oranges are fruit", "director", 1999, "country")
            movie_repository.add_movie("fruity loops", "director", 1999, "country")
            movie_repository.add_movie("Fruitless", "director", 1999, "country")
            movie_repository.add_movie("Some title", "director", 1999, "country")
            movies = movie_repository.get_movies_by_word_in_title("fruit")
            assert len(movies) == 3

    def test_get_movies_by_director(self):
        """Test method for getting movies by certain director"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("Oranges are fruit", "director1", 1999, "country")
            movie_repository.add_movie("fruity loops", "director2", 1999, "country")
            movie_repository.add_movie("Fruitless", "director1", 1999, "country")
            movie_repository.add_movie("Some title", "director3", 1999, "country")
            movies1 = movie_repository.get_movies_by_director("director1")
            movies2 = movie_repository.get_movies_by_director("director2")
            movies3 = movie_repository.get_movies_by_director("director3")
            assert len(movies1) == 2
            assert len(movies2) == 1
            assert len(movies3) == 1
            assert movies2[0].title == "fruity loops"


    def test_get_movies_by_release_year(self):
        """Test method for getting movies by year of release"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("Oranges are fruit", "director1", 1999, "country")
            movie_repository.add_movie("fruity loops", "director2", 2000, "country")
            movie_repository.add_movie("Fruitless", "director1", 2000, "country")
            movie_repository.add_movie("Some title", "director3", 1995, "country")
            movies = movie_repository.get_movies_by_release_year(2000)
            assert len(movies) == 2

    def test_get_movies_by_country_of_origin(self):
        """Test method for getting movies by country of origin"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("1", "director1", 1999, "country1")
            movie_repository.add_movie("2", "director2", 2000, "country1")
            movie_repository.add_movie("3", "director1", 2000, "country2")
            movie_repository.add_movie("4", "director3", 1995, "country3")
            movie_repository.add_movie("5", "director1", 2000, "country2")
            movies = movie_repository.get_movies_by_country_of_origin("country2")
            assert len(movies) == 2


    def test_get_all_directors(self):
        """Test method for getting all director names"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("1", "director1", 1999, "country1")
            movie_repository.add_movie("2", "director2", 2000, "country1")
            movie_repository.add_movie("3", "director1", 2000, "country2")
            directors = movie_repository.get_all_directors()
            assert directors == ["director1", "director2"]

    def test_get_all_titles(self):
        """Test method for getting all titles"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title 1", "director1", 1999, "country1")
            movie_repository.add_movie("title 2", "director2", 2000, "country1")
            movie_repository.add_movie("title 3", "director1", 2000, "country2")
            titles = movie_repository.get_all_titles()
            assert titles == ["title 1", "title 2", "title 3"]

    def test_change_movie_title(self):
        """Test method for changing movie title"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title 1", "director1", 1999, "country1")
            movie_repository.change_movie_title(1, "new title")
            assert movie_repository.get_title_by_id(1) == "new title"

    def test_change_movie_title_error(self):
        """Test raising error for method change movie title"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            with pytest.raises(MovieNotFound):
                movie_repository.change_movie_title(1, "title")

    def test_change_movie_title_error2(self):
        """Test raising error for method change movie title"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title 1", "director1", 1999, "country1")
            movie_repository.add_movie("title 2", "director1", 1999, "country1")
            with pytest.raises(IntegrityError):
                movie_repository.change_movie_title(1, "title 2")

    def test_change_movie_director(self):
        """Test method for changing movie director"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title 1", "director1", 1999, "country1")
            movie = movie_repository.change_movie_director(1, "new director")
            assert movie.director == "new director"

    def test_change_movie_director_error(self):
        """Test raising error for method change movie director"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            with pytest.raises(MovieNotFound):
                movie_repository.change_movie_director(1, "director")

    def test_change_movie_director_error2(self):
        """Test raising error for method change movie director"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title 1", "director1", 1999, "country1")
            movie_repository.add_movie("title 1", "director2", 1999, "country1")
            with pytest.raises(IntegrityError):
                movie_repository.change_movie_director(1, "director2")

    def test_change_movie_release_year(self):
        """Test method for changing movie release year"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title 1", "director1", 1999, "country1")
            movie = movie_repository.change_movie_release_year(1, 2000)
            assert movie.release_year == 2000

    def test_change_movie_release_year_error(self):
        """Test raising error for method change movie release year"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            with pytest.raises(MovieNotFound):
                movie_repository.change_movie_release_year(1, 2000)

    def test_change_movie_release_year_error2(self):
        """Test raising error for method change movie release year"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title 1", "director1", 1999, "country1")
            movie_repository.add_movie("title 1", "director1", 2000, "country1")
            with pytest.raises(IntegrityError):
                movie_repository.change_movie_release_year(1, 2000)

    def test_delete_movie_by_id(self):
        """Test method delete movie by id"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            movie_repository.add_movie("title 1", "director1", 1999, "country1")
            assert movie_repository.delete_movie_by_id(1) is True

    def test_delete_movie_by_id_error(self):
        """Test raising error for method delete movie by id"""
        with TestingSessionLocal() as db:
            movie_repository = MovieRepository(db)
            with pytest.raises(MovieNotFound):
                movie_repository.delete_movie_by_id(1)
