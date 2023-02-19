"""Module for MovieGenre repository"""
from typing import Type
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.movie.exceptions import DuplicateDataEntry, MovieGenreNotFound
from app.movie.model import MovieGenre


class MovieGenreRepository:
    """Class for MovieGenre repository layer methods"""

    def __init__(self, dbs: Session):
        self.dbs = dbs

    def add_movie_genre(self, movie_id, genre_name: str) -> MovieGenre:
        """
        The add_movie_genre function adds a movie genre to the database.
        It takes in two parameters, movie_id and genre_name. It returns a MovieGenre object.
        """
        try:
            if self.dbs.query(MovieGenre).filter(and_(MovieGenre.movie_id == movie_id,
                                                      MovieGenre.genre_name == genre_name)).first() is not None:
                raise DuplicateDataEntry(f"Movie id {movie_id} and genre {genre_name} exist.")
            movie_genre = MovieGenre(movie_id=movie_id, genre_name=genre_name)
            self.dbs.add(movie_genre)
            self.dbs.commit()
            self.dbs.refresh(movie_genre)
            return movie_genre
        except Exception as err:
            raise err

    def get_all(self) -> list[Type[MovieGenre]]:
        """
        The get_all function returns a list of all the movie genres in the database.
        """
        movie_genre = self.dbs.query(MovieGenre).all()
        return movie_genre

    def get_all_movie_ids_of_certain_genre(self, genre_name: str) -> list[int]:
        """
        The get_all_movie_ids_of_certain_genre function takes in a genre name and returns all the movie ids of that
        genre. It does this by querying the MovieGenre table for all rows where the genre_name matches what was passed
        in, and then returning a list of those movie ids.
        """
        movie_genres = self.dbs.query(MovieGenre).filter(MovieGenre.genre_name == genre_name).all()
        movie_ids = [movie_genre.movie_id for movie_genre in movie_genres]
        return movie_ids

    def delete_movie_genre(self, movie_id: int, genre_name: str) -> bool:
        movie = self.dbs.query(MovieGenre).filter \
            (and_(MovieGenre.movie_id == movie_id, MovieGenre.genre_name == genre_name)).first()
        if movie is None:
            raise MovieGenreNotFound(f"There is no genre {genre_name} for movie with id {movie_id}")
        self.dbs.delete(movie)
        self.dbs.commit()
        return True
