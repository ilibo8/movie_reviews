from fastapi import APIRouter
from app.movie.controller import MovieController
from app.movie.schema import MovieSchema, MovieGenreSchema

movie_router = APIRouter(prefix="/api/movies", tags=["Movies"])


@movie_router.get("/get-all-movies", response_model=list[MovieSchema])
def get_all_movies():
    return MovieController.get_all_movies()


@movie_router.get("/get-genres-od-movie/{movie_id}", response_model=list[MovieGenreSchema])
def get_genres_of_movie(movie_id : int):
    return MovieController.get_genre_of_movie(movie_id)
