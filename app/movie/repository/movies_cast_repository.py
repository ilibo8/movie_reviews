"""Module for MovieCast repository"""
from typing import Type
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.actor.model import Actor
from app.movie.exceptions import DuplicateDataEntry, MovieNotFound, MovieCastNotFound
from app.movie.model import MovieCast, Movie


class MovieCastRepository:
    """Class for MovieCast repository layer methods"""
    def __init__(self, db: Session):
        self.db = db

    def add(self, movie_id: int, actor_id: int) -> MovieCast:
        """
        The add function adds a new movie cast to the database.
        If the given combination of movie id and actor id already exists in the database, it raises an error.
        """
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
        """
        The get_all function returns a list of all the movie_cast objects in the database.
        The get_all function is called by passing no arguments to it, and it returns a list of MovieCast objects.
        """
        movies_cast = self.db.query(MovieCast).order_by(MovieCast.movie_id).all()
        return movies_cast

    def get_cast_ids_by_movie_id(self, movie_id: int) -> list[int]:
        """
        The get_cast_ids_by_movie_id function accepts a movie_id as an argument and returns a list of cast ids for
        the given movie. If no such movie exists, it raises MovieNotFound exception.
        """
        if self.db.query(Movie).filter(Movie.id == movie_id).first() is None:
            raise MovieNotFound(f"No movie id {movie_id}")
        movie_cast = self.db.query(MovieCast).filter(MovieCast.movie_id == movie_id).all()
        cast_ids = [movie.actor_id for movie in movie_cast]
        return cast_ids

    def get_movie_ids_by_actor_id(self, actor_id: int) -> list[int]:
        """
        The get_movie_ids_by_actor_id function takes an actor_id as a parameter and returns a list of movie ids
        for all the movies that the actor has been in. If no movies are found, it raises MovieNotFound exception.
        """
        if self.db.query(Actor).filter(Actor.id == actor_id).first() is None:
            raise MovieNotFound(f"No actor with id {actor_id}")
        movie_cast = self.db.query(MovieCast).filter(MovieCast.actor_id == actor_id).all()
        movies_ids = [movie.movie_id for movie in movie_cast]
        return movies_ids

    def get_movies_by_actor_id(self, actor_id: int) -> list[Type[MovieCast]]:
        """
        The function takes an actor_id as a parameter and returns a list of movie that the actor has been in.
        """
        return self.db.query(MovieCast).filter(MovieCast.actor_id == actor_id).all()

    def delete_movie_cast(self, movie_id: int, actor_id: int) -> bool:
        """
        The delete_movie_cast function deletes a movie cast from the database.
        It takes two arguments, movie_id and actor_id. It returns True if the deletion was successful.
        """
        movie = self.db.query(MovieCast).filter \
            (and_(MovieCast.movie_id == movie_id, MovieCast.actor_id == actor_id)).first()
        if movie is None:
            raise MovieCastNotFound(f"There is no actor id {actor_id} in cast for movie with id {movie_id}")
        self.db.delete(movie)
        self.db.commit()
        return True
