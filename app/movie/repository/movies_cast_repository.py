from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.movie.model import MovieCast


class MovieCastRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        movies_cast = self.db.query(MovieCast).all
        return movies_cast

    def add(self, movie_id, actor_name):
        try:
            movie_cast = MovieCast(movie_id, actor_name)
            self.db.add(movie_cast)
            self.db.commit()
            self.db.refresh(movie_cast)
            return movie_cast
        except IntegrityError as e:
            raise e
