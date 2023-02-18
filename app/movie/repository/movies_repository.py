from typing import Type
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.movie.exceptions import MovieNotFound
from app.movie.model import Movie


class MovieRepository:

    def __init__(self, db: Session):
        self.db = db

    def add_movie(self, title: str, director: str, release_year: int, country_of_origin: str) -> Movie:
        """Method for adding a movie in database."""
        try:
            movie = Movie(title, director, release_year, country_of_origin)
            self.db.add(movie)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        except IntegrityError as e:
            raise e

    def get_all_movies(self) -> list[Type[Movie]]:
        """Get list of all movies."""
        return self.db.query(Movie).order_by(Movie.id).all()

    def get_all_movies_order_by_name(self) -> list[Type[Movie]]:
        """Get list of all movies."""
        return self.db.query(Movie).order_by(Movie.title).all()

    def get_movie_by_id(self, movie_id: int) -> Movie:
        """Get movie by id."""
        movie = self.db.query(Movie).get(movie_id)
        return movie

    def get_movie_by_title(self, movie_title: str) -> Type[Movie] | None:
        """Get movie by id."""
        movie = self.db.query(Movie).filter(Movie.title == movie_title).first()
        return movie

    def get_title_by_id(self, movie_id: int) -> str:
        """Get title for movie by id."""
        title = self.db.query(Movie.title).filter(Movie.id == movie_id).first()
        return title[0]

    def get_movie_id_by_title(self, title: str) -> int:
        movie = self.db.query(Movie).filter(func.lower(Movie.title) == title.lower()).first()
        if movie is None:
            raise MovieNotFound(f"There is no movie with title {title}")
        return movie.id

    def get_movies_by_word_in_title(self, word: str) -> list[Type[Movie]]:
        """Get list of movies with chosen word in title."""
        movies = self.db.query(Movie).filter(Movie.title.ilike(f'%{word}%')).all()
        return movies

    def get_movies_by_director(self, director: str) -> list[Type[Movie]]:
        """Get list of movies by director."""

        movies = self.db.query(Movie).filter(Movie.director.contains(director)).all()
        if movies is None:
            raise MovieNotFound("No movies by that director found.")
        return movies

    def get_movies_by_release_year(self, release_year: int) -> list[Type[Movie]]:
        """Get list of movies by release year."""
        movies = self.db.query(Movie).filter(Movie.release_year == release_year).all()
        if movies is None:
            raise MovieNotFound(f"No movies with release year {release_year} found.")
        return movies

    def get_movies_by_country_of_origin(self, country_of_origin: str) -> list[Type[Movie]]:
        """Get list of movies by country of origin."""
        movies = self.db.query(Movie).filter(Movie.country_of_origin == country_of_origin).all()
        if movies is None:
            raise MovieNotFound(f"No movies from {country_of_origin} in database.")
        return movies

    def get_all_directors(self):
        """Returns list of all directors in database."""
        return self.db.query(Movie.director.distinct()).all()

    def get_all_countries_of_origin(self):
        """Returns list of all countries of movie origin"""
        return self.db.query(Movie.country_of_origin.distinct()).all()

    def get_all_titles(self):
        """Returns list of all movie titles."""
        return self.db.query(Movie.title).all()

    def change_movie_title(self, movie_id: int, title: str) -> (Movie, None):
        """Method for changing movie title"""
        try:
            movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
            if movie is None:
                raise MovieNotFound(f"There is no movie with id {movie_id}")
            movie.title = title
            self.db.add(movie)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        except IntegrityError as e:
            raise e

    def change_movie_director(self, movie_id: int, director: str) -> (Movie, None):
        """Method for changing movie director."""
        try:
            movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
            if movie is None:
                raise MovieNotFound(f"There is no movie with id {movie_id}")
            movie.director = director
            self.db.add(movie)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        except IntegrityError as e:
            raise e

    def change_movie_release_year(self, movie_id: int, release_year: int) -> (Movie, None):
        """Method for changing movie release year"""
        try:
            movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
            if movie is None:
                raise MovieNotFound(f"There is no movie with id {movie_id}")
            movie.release_year = release_year
            self.db.add(movie)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        except IntegrityError as e:
            raise e

    def change_movie_country_of_origin(self, movie_id: int, country_of_origin: str) -> (Movie, None):
        """Method for changing country of origin for movie."""
        try:
            movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
            if movie is None:
                raise MovieNotFound(f"There is no movie with id {movie_id}")
            movie.country_of_origin = country_of_origin
            self.db.add(movie)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        except IntegrityError as e:
            raise e

    def delete_movie_by_id(self, movie_id: int) -> bool:
        """Delete movie by id."""
        movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if movie is None:
            raise MovieNotFound(f"There is no movie with id {movie_id}.")
        self.db.delete(movie)
        self.db.commit()
        return True
