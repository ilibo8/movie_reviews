from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from app.movie.exceptions import NotFoundException, DuplicateDataEntryException
from app.movie.model import MovieGenre


class MovieGenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_movie_genre(self, movie_id, genre_name: str) -> MovieGenre:
        try:
            if self.db.query(MovieGenre).filter(and_(MovieGenre.movie_id == movie_id,
                                                     MovieGenre.genre_name == genre_name)).first() is not None:
                raise DuplicateDataEntryException(f"Movie id {movie_id} and genre {genre_name} exist.")
            movie_genre = MovieGenre(movie_id=movie_id, genre_name=genre_name)
            self.db.add(movie_genre)
            self.db.commit()
            self.db.refresh(movie_genre)
            return movie_genre
        except Exception as e:
            raise e

    def get_all(self) -> list[MovieGenre]:
        movie_genre = self.db.query(MovieGenre).all()
        return movie_genre

    def get_all_movie_ids_of_certain_genre(self, genre_name: str) -> list[tuple]:
        try:
            movie_ids = self.db.query(MovieGenre.movie_id).filter(MovieGenre.genre_name == genre_name).all()
            return movie_ids
        except IntegrityError as e:
            raise e

    def delete_movie_genre(self, movie_id: int, genre_name: str) -> bool:
        try:
            movie = self.db.query(MovieGenre).filter\
                (and_(MovieGenre.movie_id == movie_id, MovieGenre.genre_name == genre_name)).first()
            if movie is None:
                raise NotFoundException(f"There is no movie with id {movie_id} and genre {genre_name}")
            self.db.delete(movie)
            self.db.commit()
            return True
        except Exception as e:
            raise e
