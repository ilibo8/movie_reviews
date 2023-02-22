"""Module for Genre routes"""
from fastapi import APIRouter, Depends
from app.genre.controller import GenreController
from app.genre.schema import GenreSchema
from app.users.controller import JWTBearer

genre_superuser_router = APIRouter(prefix="/api/superuser/movies/genres", tags=["superuser - Actors & Genre"])


@genre_superuser_router.get("/get-all", response_model=list[str], dependencies=[Depends(JWTBearer("super_user"))])
def get_all_genre():
    """
    The function returns a list of all genres in the database.
    """
    return GenreController.get_all_genres()


@genre_superuser_router.post("/add-genre", response_model=GenreSchema, dependencies=[Depends(JWTBearer("super_user"))])
def add_genre(genre: GenreSchema):
    """
    The function adds a new genre to the database.
    """
    return GenreController.add_genre(genre.name)


@genre_superuser_router.delete("/delete-genre", dependencies=[Depends(JWTBearer("super_user"))])
def delete(name: str):
    """
    The function deletes genre from the database.
    """
    return GenreController.delete(name)
