from typing import Type

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.actor.model import Actor
from app.movie.exceptions import DuplicateDataEntry, MovieNotFound, MovieCastNotFound
from app.movie.model import MovieCast, Movie


class MovieCastRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, movie_id: int, actor_id: int) -> MovieCast:
        try:
            if self.db.query(MovieCast).filter(and_(MovieCast.movie_id == movie_id,
                                                    MovieCast.actor_id == actor_id)).first() is not None:
                raise DuplicateDataEntry(f"Movie id {movie_id} already has actor id {actor_id}.")
            movie_cast = MovieCast(movie_id,  actor_id)
            self.db.add(movie_cast)
            self.db.commit()
            self.db.refresh(movie_cast)
            return movie_cast
        except Exception as err:
            raise err

    def get_all(self) -> list[Type[MovieCast]]:
        movies_cast = self.db.query(MovieCast).order_by(MovieCast.movie_id).all()
        return movies_cast

    def get_cast_ids_by_movie_id(self, movie_id: int) -> list[int]:
        if self.db.query(Movie).filter(Movie.id == movie_id).first() is None:
            raise MovieNotFound(f"No movie id {movie_id}")
        movie_cast = self.db.query(MovieCast).filter(MovieCast.movie_id == movie_id).all()
        cast_ids = [movie.actor_id for movie in movie_cast]
        return cast_ids

    def get_movie_ids_by_actor_id(self, actor_id: int) -> list[int]:
        if self.db.query(Actor).filter(Actor.id == actor_id).first() is None:
            raise MovieNotFound(f"No actor with id {actor_id}")
        movie_cast = self.db.query(MovieCast).filter(MovieCast.actor_id == actor_id).all()
        movies_ids = [movie.movie_id for movie in movie_cast]
        return movies_ids

    def delete_movie_cast(self, movie_id: int, actor_id: int) -> bool:
        movie = self.db.query(MovieCast).filter \
            (and_(MovieCast.movie_id == movie_id, MovieCast.actor_id == actor_id)).first()
        if movie is None:
            raise MovieCastNotFound(f"There is no actor id {actor_id} in cast for movie with id {movie_id}")
        self.db.delete(movie)
        self.db.commit()
        return True
