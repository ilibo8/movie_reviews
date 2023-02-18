from typing import Type

from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.movie.exceptions import DuplicateDataEntry, MovieGenreNotFound
from app.movie.model import MovieGenre


class MovieGenreRepository:
    """Repository for movie genre."""
    def __init__(self, db: Session):
        self.db = db

    def add_movie_genre(self, movie_id, genre_name: str) -> MovieGenre:
        try:
            if self.db.query(MovieGenre).filter(and_(MovieGenre.movie_id == movie_id,
                                                     MovieGenre.genre_name == genre_name)).first() is not None:
                raise DuplicateDataEntry(f"Movie id {movie_id} and genre {genre_name} exist.")
            movie_genre = MovieGenre(movie_id=movie_id, genre_name=genre_name)
            self.db.add(movie_genre)
            self.db.commit()
            self.db.refresh(movie_genre)
            return movie_genre
        except Exception as err:
            raise err

    def get_all(self) -> list[Type[MovieGenre]]:
        movie_genre = self.db.query(MovieGenre).all()
        return movie_genre

    def get_all_movie_ids_of_certain_genre(self, genre_name: str) -> list[int]:
        movie_genres = self.db.query(MovieGenre).filter(MovieGenre.genre_name == genre_name).all()
        movie_ids = [movie_genre.movie_id for movie_genre in movie_genres]
        return movie_ids

    def delete_movie_genre(self, movie_id: int, genre_name: str) -> bool:
        movie = self.db.query(MovieGenre).filter\
            (and_(MovieGenre.movie_id == movie_id, MovieGenre.genre_name == genre_name)).first()
        if movie is None:
            raise MovieGenreNotFound(f"There is no genre {genre_name} for movie with id {movie_id}")
        self.db.delete(movie)
        self.db.commit()
        return True
