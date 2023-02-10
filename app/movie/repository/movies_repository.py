from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.movie.exceptions import MovieNotFound
from app.movie.model import Movie


class MovieRepository:

    def __init__(self, db: Session):
        self.db = db

    def add_movie(self, title: str, director: str, release_year: int, country_of_origin: str) -> Movie:
        try:
            movie = Movie(title, director, release_year, country_of_origin)
            self.db.add(movie)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        except IntegrityError as e:
            raise e

    def get_all_movies(self) -> list[Movie]:
        return self.db.query(Movie).all()

    def get_movie_by_id(self, movie_id: int) -> Movie:
        movie = self.db.query(Movie).get(movie_id)
        return movie

    def get_title_by_id(self, movie_id: int) -> tuple:
        return self.db.query(Movie.title).filter(Movie.id == movie_id).first()

    def get_movies_by_word_in_title(self, word: str) -> list[Movie]:
        movies = self.db.query(Movie).filter(Movie.title.ilike(f'%{word}%')).all()
        return movies

    def get_movies_by_director(self, director: str) -> list[Movie]:
        movies = self.db.query(Movie).filter(Movie.director.contains(director)).all()
        if movies is None:
            raise MovieNotFound("No movies by that director found.")
        return movies

    def get_movies_by_release_year(self, release_year: int) -> list[Movie]:
        movies = self.db.query(Movie).filter(Movie.release_year == release_year).all()
        if movies is None:
            raise MovieNotFound(f"No movies with release year {release_year} found.")
        return movies

    def get_movies_by_country_of_origin(self, country_of_origin: str) -> list[Movie]:
        movies = self.db.query(Movie).filter(Movie.country_of_origin == country_of_origin).all()
        if movies is None:
            raise MovieNotFound(f"No movies from {country_of_origin} in database.")
        return movies

    def get_all_directors(self):
        return self.db.query(Movie.director.distinct()).all()

    def get_all_countries_of_origin(self):
        return self.db.query(Movie.country_of_origin.distinct()).all()

    def get_all_titles(self):
        return self.db.query(Movie.title).all()

    def change_movie_title(self, movie_id: int, title: str) -> (Movie, None):
        movie = self.db.query(Movie.id == movie_id).first()
        if movie is None:
            raise MovieNotFound(f"There is no movie with id {movie_id}")
        movie.title = title
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def change_movie_director(self, movie_id: int, director: str) -> (Movie, None):
        movie = self.db.query(Movie.id == movie_id).first()
        if movie is None:
            raise MovieNotFound(f"There is no movie with id {movie_id}")
        movie.director = director
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def change_movie_release_year(self, movie_id: int, release_year: int) -> (Movie, None):
        movie = self.db.query(Movie.id == movie_id).first()
        if movie is None:
            raise MovieNotFound(f"There is no movie with id {movie_id}")
        movie.release_year = release_year
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def change_movie_country_of_origin(self, movie_id: int, country_of_origin: str) -> (Movie, None):
        movie = self.db.query(Movie.id == movie_id).first()
        if movie is None:
            raise MovieNotFound(f"There is no movie with id {movie_id}")
        movie.country_of_origin = country_of_origin
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete_movie_by_id(self, movie_id: int) -> bool:
        try:
            movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
            if movie is None:
                return False
            self.db.delete(movie)
            self.db.commit()
            return True
        except Exception as e:
            raise e
