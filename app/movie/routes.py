from fastapi import APIRouter
from app.movie.controller import MovieController
from app.movie.schema import MovieSchema, MovieGenreSchema, MovieSchemaIn, MovieSchemaJoined, MovieCastSchema

movie_router = APIRouter(prefix="/api/movies", tags=["Movies"])


@movie_router.get("/get-all-movies", response_model=list[MovieSchemaJoined])
def get_all_movies():
    return MovieController.get_all_movies()


@movie_router.get("/get-movie-by-id/{movie_id}", response_model=MovieSchemaJoined)
def get_movie_by_id(movie_id: int):
    return MovieController.get_movie_by_id(movie_id)


@movie_router.get("/get-all-movies-by/word-in-title", response_model=list[MovieSchemaJoined])
def get_movies_by_word_in_title(word: str):
    return MovieController.get_movies_by_word_in_title(str(word))


@movie_router.get("/get-all-movies-by/genre/{genre}")
def get_movies_of_certain_genre(genre: str):
    return MovieController.get_movies_of_certain_genre(str(genre))


@movie_router.post("/add-movie", response_model=MovieSchema)
def add_movie(movie: MovieSchemaIn):
    return MovieController.add_movie(movie.title, movie.director, movie.release_year, movie.country_of_origin)


@movie_router.post("/add-movie-genre", response_model=MovieGenreSchema)
def add_movie_genre(movie_genre: MovieGenreSchema):
    return MovieController.add_genre_to_movie(movie_genre.movie_id, movie_genre.genre_name)


@movie_router.post("/add-movie-cast", response_model=MovieCastSchema)
def add_movie_cast(movie_cast: MovieCastSchema):
    return MovieController.add_movie_cast(movie_cast.movie_id, movie_cast.actor_id)
