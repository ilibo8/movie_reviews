"""Module for Movie repository"""
from typing import Type
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.movie.exceptions import MovieNotFound
from app.movie.model import Movie


class MovieRepository:
    """Class for Movie repository layer methods"""

    def __init__(self, dbs: Session):
        self.dbs = dbs

    def add_movie(self, title: str, director: str, release_year: int, country_of_origin: str) -> Movie:
        """
        The add_movie function adds a new movie to the database.
        It takes in four arguments: title, director, release_year and country_of_origin.
        The function returns the newly added movie.
        """
        try:
            movie = Movie(title, director, release_year, country_of_origin)
            self.dbs.add(movie)
            self.dbs.commit()
            self.dbs.refresh(movie)
            return movie
        except IntegrityError as err:
            raise err

    def get_all_movies(self) -> list[Type[Movie]]:
        """
        The get_all_movies function returns a list of all the movies in the database.
        """
        return self.dbs.query(Movie).order_by(Movie.id).all()

    def get_movie_by_id(self, movie_id: int) -> Type[Movie] | None:
        """
        The get_movie_by_id function takes a movie_id as an argument and returns the Movie object with that id.
        If no such movie is found, it raises a 404 error.
        """
        movie = self.dbs.query(Movie).filter(Movie.id == movie_id).first()
        return movie

    def get_all_movies_order_by_name(self) -> list[Type[Movie]]:
        """
        The get_all_movies_order_by_name function returns a list of all movies in the database, ordered by title.
        It takes no arguments and returns a list of Movie objects.
        """
        return self.dbs.query(Movie).order_by(Movie.title).all()

    def get_movie_by_title(self, movie_title: str) -> Type[Movie] | None:
        """
        The get_movie_by_title function takes a movie title as an argument and returns the Movie object
        associated with that title if it exists in the database. If no such movie exists, None is returned.
        """
        movie = self.dbs.query(Movie).filter(Movie.title == movie_title).first()
        return movie

    def get_title_by_id(self, movie_id: int) -> str:
        """
        The get_title_by_id function takes a movie id as an argument and returns the title of that movie.
        """
        title = self.dbs.query(Movie.title).filter(Movie.id == movie_id).first()
        return title[0]

    def get_movie_id_by_title(self, title: str) -> int:
        """
        The get_movie_id_by_title function takes a string title and returns the movie id of the movie with that title.
        If no such movie exists, it raises a MovieNotFound exception.
        """
        movie = self.dbs.query(Movie).filter(func.lower(Movie.title) == title.lower()).first()
        if movie is None:
            raise MovieNotFound(f"There is no movie with title {title}")
        return movie.id

    def get_movies_by_word_in_title(self, word: str) -> list[Type[Movie]]:
        """
        The get_movies_by_word_in_title function takes a word as an argument and returns a list of movies whose
        titles contain that word.
        """
        movies = self.dbs.query(Movie).filter(Movie.title.ilike(f'%{word}%')).all()
        return movies

    def get_movies_by_director(self, director: str) -> list[Type[Movie]]:
        """
        The get_movies_by_director function takes a director's name as an argument and returns all movies by that
        director. If no movies are found, it raises a MovieNotFound exception.
        """
        movies = self.dbs.query(Movie).filter(Movie.director.contains(director)).all()
        if len(movies) == 0:
            raise MovieNotFound("No movies by that director found.")
        return movies

    def get_movies_by_release_year(self, release_year: int) -> list[Type[Movie]]:
        """
        The get_movies_by_release_year function returns a list of movies that match the release year provided
        by the user. If no movies are found, it raises an exception.
        """
        movies = self.dbs.query(Movie).filter(Movie.release_year == release_year).all()
        if len(movies) == 0:
            raise MovieNotFound(f"No movies with release year {release_year} found.")
        return movies

    def get_movies_by_country_of_origin(self, country_of_origin: str) -> list[Type[Movie]]:
        """
        The get_movies_by_country_of_origin function returns a list of movies from the given country.
        If no movies are found, it raises an exception.
        """
        movies = self.dbs.query(Movie).filter(Movie.country_of_origin == country_of_origin).all()
        if len(movies) == 0:
            raise MovieNotFound(f"No movies from {country_of_origin} in database.")
        return movies

    def get_all_directors(self) -> list[str]:
        """
        The get_all_directors function returns a list of all the distinct directors in the database.
        It does this by querying the Movie table and selecting only distinct values from the director column.
        """
        directors_tuple = self.dbs.query(Movie.director.distinct()).all()
        directors = [x[0] for x in directors_tuple]
        directors.sort()
        return directors

    def get_all_titles(self) -> list[str]:
        """
        The get_all_titles function returns a list of all the movie titles in the database.
        It takes no arguments and returns a list of tuples, where each tuple is (title).
        """
        titles_tuple = self.dbs.query(Movie.title).all()
        titles = [x[0] for x in titles_tuple]
        titles.sort()
        return titles

    def change_movie_title(self, movie_id: int, title: str) -> (Movie, None):
        """
        The change_movie_title function takes a movie_id and a title as arguments.
        It then checks if the movie exists in the database, and if it does, changes its title to the new one.
        If there is no such movie in the database, it raises an error.
        """
        try:
            movie = self.dbs.query(Movie).filter(Movie.id == movie_id).first()
            if movie is None:
                raise MovieNotFound(f"There is no movie with id {movie_id}")
            movie.title = title
            self.dbs.add(movie)
            self.dbs.commit()
            self.dbs.refresh(movie)
            return movie
        except IntegrityError as err:
            raise err

    def change_movie_director(self, movie_id: int, director: str) -> (Movie, None):
        """
        The change_movie_director function takes in a movie id and a director name.
        It then checks if the movie exists in the database, and if it does, changes its director to the new one.
        If there is no such movie with that id, it raises an error.
        """
        try:
            movie = self.dbs.query(Movie).filter(Movie.id == movie_id).first()
            if movie is None:
                raise MovieNotFound(f"There is no movie with id {movie_id}")
            movie.director = director
            self.dbs.add(movie)
            self.dbs.commit()
            self.dbs.refresh(movie)
            return movie
        except IntegrityError as err:
            raise err

    def change_movie_release_year(self, movie_id: int, release_year: int) -> (Movie, None):
        """
        The change_movie_release_year function updates the release year of a movie.
        It takes two arguments:
            - movie_id: The id of the movie to be updated.
            - release_year: The new value for the release year field.
        """
        try:
            movie = self.dbs.query(Movie).filter(Movie.id == movie_id).first()
            if movie is None:
                raise MovieNotFound(f"There is no movie with id {movie_id}")
            movie.release_year = release_year
            self.dbs.add(movie)
            self.dbs.commit()
            self.dbs.refresh(movie)
            return movie
        except IntegrityError as err:
            raise err

    def delete_movie_by_id(self, movie_id: int) -> bool:
        """
        The delete_movie_by_id function deletes a movie from the database.
        It takes in an integer representing the id of the movie to be deleted, and returns True if it is successful.
        """
        movie = self.dbs.query(Movie).filter(Movie.id == movie_id).first()
        if movie is None:
            raise MovieNotFound(f"There is no movie with id {movie_id}.")
        self.dbs.delete(movie)
        self.dbs.commit()
        return True
