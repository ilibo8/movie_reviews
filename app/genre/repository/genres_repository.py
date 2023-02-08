from sqlalchemy.orm import Session
from app.genre.exceptions import GenreNotFoundException
from app.genre.model import Genre


class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_genre(self, name: str):
        try:
            genre = Genre(name)
            self.db.add(genre)
            self.db.commit()
            self.db.refresh(genre)
            return genre
        except Exception as e:
            raise e

    def get_all_genres(self):
        return self.db.query(Genre).all()

    def delete(self, name: str):
        try:
            genre = self.db.query(Genre).filter(Genre.name == name).first()
            if genre is None:
                raise GenreNotFoundException(f"There is no {name} entry.")
            self.db.delete(genre)
            self.db.commit()
            return True
        except Exception as e:
            raise e

    def check_is_there(self, name) -> bool:
        if self.db.query(Genre).filter(Genre.name == name).first() is None:
            return False
        return True
