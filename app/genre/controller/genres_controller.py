"""Module for Genre controller layer."""
from fastapi import HTTPException, Response
from app.genre.exceptions import GenreAlreadyExists, NoEntryForGenre, GenreNotFound
from app.genre.service import GenreService


class GenreController:
    """Class for Genre controller layer."""

    @staticmethod
    def add_genre(name: str):
        """
        The add_genre function adds a new genre to the database.
        It takes one argument, name, which is the name of the genre to be added.
        If there already exists a genre with that name in the database, an error will be raised.

        :param name:str: Specify the name of the genre to be added
        :return: A genre object
        """
        try:
            genre = GenreService.add_genre(name)
            return genre
        except GenreAlreadyExists as err:
            raise HTTPException(status_code=400, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all_genres():
        """
        The get_all_genres function returns a list of all the genres in the database.

        :return: A list of all genres in the database

        """
        try:
            genre_names = []
            genres = GenreService.get_all_genres()
            for genre in genres:
                genre_names.append(genre.name)
            return genre_names
        except NoEntryForGenre as err:
            raise HTTPException(status_code=400, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def delete(name: str):
        """
        The delete function deletes a genre from the database.
        It takes one argument, name, which is the name of the genre to be deleted.
        If successful, it returns a message that says Genre {name} is deleted.

        :param name:str: Specify the name of the genre to be deleted
        :return: A response object
        """
        try:
            if GenreService.delete(name):
                return Response(content=f"Genre {name} is deleted", status_code=200)
        except GenreNotFound as err:
            raise HTTPException(status_code=400, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
