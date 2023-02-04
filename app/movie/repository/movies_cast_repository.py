from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.movie.model import MovieCast


class MovieCastRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, movie_id, actor_name) -> MovieCast:
        try:
            movie_cast = MovieCast(movie_id, actor_name)
            self.db.add(movie_cast)
            self.db.commit()
            self.db.refresh(movie_cast)
            return movie_cast
        except IntegrityError as e:
            raise e

    def get_all(self) -> list[MovieCast]:
        movies_cast = self.db.query(MovieCast).all()
        return movies_cast

    def get_cast_ids_by_movie_id(self, movie_id):
        movie_cast = self.db.query(MovieCast.actor_id).filter(MovieCast.movie_id == movie_id).all()
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

