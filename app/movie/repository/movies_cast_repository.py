from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.actor.model import Actor
from app.movie.exceptions import DuplicateDataEntryException, NotFoundException
from app.movie.model import MovieCast, Movie


class MovieCastRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, movie_id: int, actor_id: int) -> MovieCast:
        try:
            if self.db.query(MovieCast).filter(and_(MovieCast.movie_id == movie_id,
                                                    MovieCast.actor_id == actor_id)).first() is not None:
                raise DuplicateDataEntryException(f"Movie id {movie_id} already has actor id {actor_id}.")
            movie_cast = MovieCast(movie_id,  actor_id)
            self.db.add(movie_cast)
            self.db.commit()
            self.db.refresh(movie_cast)
            return movie_cast
        except Exception as e:
            raise e

    def get_all(self) -> list[MovieCast]:
        movies_cast = self.db.query(MovieCast).all()
        return movies_cast

    def get_cast_ids_by_movie_id(self, movie_id: int) -> list[tuple]:
        if self.db.query(Movie).filter(Movie.id == movie_id).first() is None:
            raise NotFoundException(f"No movie id {movie_id}")
        movie_cast = self.db.query(MovieCast.actor_id).filter(MovieCast.movie_id == movie_id).all()
        return movie_cast

    def get_movie_ids_by_actor_id(self, actor_id: int) -> list[tuple]:
        if self.db.query(Actor).filter(Actor.id == actor_id).first() is None:
            raise NotFoundException(f"No actor with id {actor_id}")
        movie_cast = self.db.query(MovieCast.movie_id).filter(MovieCast.actor_id == actor_id).all()
        return movie_cast

    def delete_movie_cast(self, movie_id: int, actor_id: int) -> bool:
        try:
            movie = self.db.query(MovieCast).filter \
                (and_(MovieCast.movie_id == movie_id, MovieCast.actor_id == actor_id)).first()
            if movie is None:
                return False
            self.db.delete(movie)
            self.db.commit()
            return True
        except Exception as e:
            raise e
