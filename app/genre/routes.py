"""Module for Genre routes"""
from fastapi import APIRouter
from app.genre.controller import GenreController
from app.genre.schema import GenreSchema

genre_superuser_router = APIRouter(prefix="/api/superuser/movies/genres", tags=["SuperUser - Movies - Genre"])


@genre_superuser_router.get("/get-all", response_model=list[str])#
def get_all_genre():
    """
    The get_all_genre function returns all the genres in the database.

    :return: A list of all the genres in the database
    """
    return GenreController.get_all_genres()


@genre_superuser_router.post("/add-genre", response_model=GenreSchema)
def add_genre(genre: GenreSchema):
    """
    The add_genre function adds a new genre to the database.

    :param genre:GenreSchema: Pass the genre name from the schema to the controller
    :return: A genreschema object
    """
    return GenreController.add_genre(genre.name)


@genre_superuser_router.delete("/delete-genre")
def delete(name: str):
    """
    The delete function will delete a genre from the database.

    :param name:str: Specify the name of the genre to be deleted
    :return: The number of rows deleted
    """
    return GenreController.delete(name)
