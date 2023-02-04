from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.movie.model import MovieGenre


class MovieGenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[MovieGenre]:
        movie_genre = self.db.query(MovieGenre).all()
        return movie_genre

    def add_movie_genre(self, movie_id, genre_name) -> MovieGenre:
        try:
            genre = MovieGenre(movie_id=movie_id, genre_name=genre_name)
            self.db.add(genre)
            self.db.commit()
            self.db.refresh(genre)
            return genre
        except IntegrityError as e:
            raise e

    def get_genre_of_movie(self, movie_id: int) -> list[MovieGenre]:
        movie_genres = self.db.query(MovieGenre).filter(MovieGenre.movie_id == movie_id).all()
        return movie_genres

    def delete_movie_genre(self, movie_id: int, genre_name : str) -> bool:
        try:
            movie = self.db.query(MovieGenre).filter\
                (and_(MovieGenre.movie_id == movie_id, MovieGenre.genre_name == genre_name)).first()
            if movie is None:
                return False
            self.db.delete(movie)
            self.db.commit()
            return True
        except Exception as e:
            raise e
