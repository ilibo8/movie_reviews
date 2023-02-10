from app.db import SessionLocal
from app.genre.exceptions import NoEntryForGenre, GenreAlreadyExists, GenreNotFound

from app.genre.repository import GenreRepository


class GenreService:

    @staticmethod
    def add_genre(name: str):
        try:
            with SessionLocal() as db:
                genre_repository = GenreRepository(db)
                if genre_repository.check_is_there(name):
                    raise GenreAlreadyExists
                return genre_repository.add_genre(name)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_genres():
        try:
            with SessionLocal() as db:
                genre_repository = GenreRepository(db)
                genres = genre_repository.get_all_genres()
                if genres is None:
                    raise NoEntryForGenre
                return genres
        except Exception as e:
            raise e

    @staticmethod
    def delete(name: str):
        try:
            with SessionLocal() as db:
                genre_repository = GenreRepository(db)
                if genre_repository.delete(name):
                    return True
                raise GenreNotFound(f'There is no genre with name {name} in database.')
        except Exception as e:
            raise e
