"""Module for Genre routes"""
from fastapi import APIRouter
from app.genre.controller import GenreController
from app.genre.schema import GenreSchema

genre_superuser_router = APIRouter(prefix="/api/superuser/movies/genres", tags=["SuperUser - Genre"])


@genre_superuser_router.get("/get-all", response_model=list[str])#
def get_all_genre():
    return GenreController.get_all_genres()


@genre_superuser_router.post("/add-genre", response_model=GenreSchema)
def add_genre(genre: GenreSchema):

    return GenreController.add_genre(genre.name)


@genre_superuser_router.delete("/delete-genre")
def delete(name: str):
    return GenreController.delete(name)
