from fastapi import APIRouter

from app.genre.controller import GenreController
from app.genre.schema import GenreSchema

genre_router = APIRouter(prefix="/api/movies/genres", tags=["Movies - Genre"])


@genre_router.get("/get-all", response_model=list[str])
def get_all_genre():
    return GenreController.get_all_genres()


@genre_router.post("/add-genre", response_model=GenreSchema)
def add_genre(genre: GenreSchema):
    return GenreController.add_genre(genre.name)


@genre_router.delete("/delete-genre")
def delete(name: str):
    return GenreController.delete(name)
