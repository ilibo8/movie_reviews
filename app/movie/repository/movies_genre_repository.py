from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.movie.model import MovieGenre


class MovieGenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        movie_genre = self.db.query(MovieGenre).all
        return movie_genre

    def add(self, movie_id, genre_name):
        try:
            genre = MovieGenre(movie_id=movie_id, genre_name=genre_name)
            self.db.add(genre)
            self.db.commit()
            self.db.refresh(genre)
            return genre
        except IntegrityError as e:
            raise e

    def get_genre_of_movie(self, movie_id):
        movie_genres = self.db.query(MovieGenre).filter(MovieGenre.movie_id == movie_id).all
        return movie_genres
