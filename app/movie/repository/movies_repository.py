from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.movie.exceptions import MovieNotFoundException
from app.movie.model import Movie


class MovieRepository:

    def __init__(self, db: Session):
        self.db = db

    def add_movie(self, title: str, director: str, release_year: int, country_of_origin: str):
        try:
            movie = Movie(title, director, release_year, country_of_origin)
            self.db.add(movie)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        except IntegrityError as e:
            raise e

    def get_all_movies(self):
        return self.db.query(Movie).all()

    def get_movie_by_id(self, id: int):
        movie = self.db.query(Movie).get(id)
        if movie is None:
            raise MovieNotFoundException(f"No movie with id {id} in database.")
        return movie

    def get_movie_by_word_in_title(self, word: str):
        movie = self.db.query(Movie).filter(Movie.title.ilike(f'%{word}%')).all()
        if movie is None:
            raise MovieNotFoundException("There are no movies with that word in title.")

    def get_movie_by_director(self, director: str):
        movie = self.db.query(Movie).filter(Movie.director.contains(director)).all()
        if movie is None:
            raise MovieNotFoundException("No movies by that director found.")

    def get_movie_by_release_year(self, release_year: int):
        movie = self.db.query(Movie).filter(Movie.release_year == release_year).all()
        if movie is None:
            raise MovieNotFoundException(f"No movies with release year {release_year} found.")
        return movie

    def get_movie_by_country_of_origin(self, country_of_origin: str):
        movies = self.db.query(Movie).filter(Movie.country_of_origin == country_of_origin).all()
        if movies is None:
            raise MovieNotFoundException(f"No movies from {country_of_origin} in database.")
        return movies

    def get_all_directors(self):
        return self.db.query(Movie.director.distinct()).all()

    def get_all_countries_of_origin(self):
        return self.db.query(Movie.country_of_origin.distinct()).all()

    def get_all_titles(self):
        return self.db.query(Movie.title).all()
