"""Module for Genre service"""
from app.db import SessionLocal
from app.genre.exceptions import NoEntryForGenre, GenreAlreadyExists, GenreNotFound
from app.genre.repository import GenreRepository


class GenreService:
    """Class for Genre service layer."""

    @staticmethod
    def add_genre(name: str):
        """
        The add_genre function adds a new genre to the database.
        It takes one argument, name, which is the name of the genre to be added.
        If there is already a genre with that name in the database, it raises GenreAlreadyExists.
        """
        try:
            with SessionLocal() as db:
                genre_repository = GenreRepository(db)
                if genre_repository.check_is_there(name):
                    raise GenreAlreadyExists
                return genre_repository.add_genre(name)
        except Exception as err:
            raise err

    @staticmethod
    def get_all_genres():
        """
        The get_all_genres function returns a list of all genres in the database.
        """
        try:
            with SessionLocal() as db:
                genre_repository = GenreRepository(db)
                genres = genre_repository.get_all_genres()
                if genres is None:
                    raise NoEntryForGenre
                return genres
        except Exception as err:
            raise err

    @staticmethod
    def delete(name: str):
        """
        The delete function takes a name as an argument and deletes the genre with that name from the database.
        If no such genre exists, it raises a GenreNotFound exception.
        """
        try:
            with SessionLocal() as db:
                genre_repository = GenreRepository(db)
                if genre_repository.delete(name):
                    return True
                raise GenreNotFound(f'There is no genre with name {name} in database.')
        except Exception as err:
            raise err
