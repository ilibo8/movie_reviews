"""Module for Movie routes"""
from fastapi import APIRouter, Depends
from app.movie.controller import MovieController
from app.movie.schema import MovieSchemaJoined, MovieSchemaIn, MovieCastSchema, MovieSchemaAll, MovieSchema, \
    MovieGenreSchema, MovieSchemaUpdateTitle, MovieSchemaUpdateDirector, MovieSchemaUpdateReleaseYear
from app.users.controller import JWTBearer

movie_router = APIRouter(prefix="/api/movies", tags=["Movies"])
movie_superuser_router = APIRouter(prefix="/api/superuser/movies", tags=["superuser - Movies"])


@movie_router.get("/get-all-movies", response_model=list[MovieSchemaJoined])
def get_all_movies():
    """
    The function returns a list of all movies in the database.
    """
    return MovieController.get_all_movies()


@movie_router.get("/get-movie-by-title/{movie_title}", response_model=MovieSchemaJoined)
def get_movie_by_title(movie_title: str):
    """
    The function takes a movie title as an argument and returns the movie with that title.
    """
    return MovieController.get_movie_by_title(movie_title)


@movie_router.get("/get-all-movies-by/word-in-title", response_model=list[MovieSchemaJoined])
def get_movies_by_word_in_title(word: str):
    """
    The function takes a word as an argument and returns all movies that contain the word in their title.
    """
    return MovieController.get_movies_by_word_in_title(str(word))


@movie_router.get("/get-movies-by/actor-full-name/{actor_full_name}", response_model=list[MovieSchemaJoined])
def get_movies_by_actor_full_name(actor_full_name: str):
    """
    The function takes an actor's full name as a string and returns all movies that the actor has been in.
    """
    return MovieController.get_movies_by_actor_full_name(actor_full_name)


@movie_router.get("/get-all-movies-by/genre/{genre}")
def get_movies_of_certain_genre(genre: str):
    """
    The function takes a genre as an argument and returns all movies of that genre.
    """
    return MovieController.get_movies_of_certain_genre(str(genre))


@movie_router.get("/get-all/directors", response_model=list)
def get_all_directors():
    """
    The function returns a list of all directors in the database.
    """
    return MovieController.get_all_directors()


@movie_router.get("/get-all-movies-by/director", response_model=list[MovieSchemaIn])
def get_all_movies_by_director(director_name: str):
    """
    The function returns a list of all movies by the given director.
    """
    return MovieController.get_all_movies_by_director(director_name)


@movie_superuser_router.get("/get-all-movies", response_model=list[MovieSchemaAll],
                            dependencies=[Depends(JWTBearer("super_user"))])
def get_all_movies_with_cast_and_genre():
    """
    The function returns all movies in the database with their cast and genre.
    """
    return MovieController.get_all()


@movie_superuser_router.get("/get-all-movie_cast", response_model=list[MovieCastSchema],
                            dependencies=[Depends(JWTBearer("super_user"))])
def get_all_movies_cast():
    """
    The function returns a list of all the movies cast members.
    """
    return MovieController.get_all_movie_cast()


@movie_superuser_router.post("/add-movie", response_model=MovieSchema, dependencies=[Depends(JWTBearer("super_user"))])
def add_movie(movie: MovieSchemaIn):
    """
    The function adds a new movie to the database.
    """
    return MovieController.add_movie(movie.title, movie.director, movie.release_year, movie.country_of_origin)


@movie_superuser_router.post("/add-movie-genre", response_model=MovieGenreSchema,
                             dependencies=[Depends(JWTBearer("super_user"))])
def add_movie_genre(movie_genre: MovieGenreSchema):
    """
    The function adds a movie genre to the database.
    """
    return MovieController.add_genre_to_movie(movie_genre.movie_id, movie_genre.genre_name)


@movie_superuser_router.post("/add-movie-cast", response_model=MovieCastSchema,
                             dependencies=[Depends(JWTBearer("super_user"))])
def add_movie_cast(movie_cast: MovieCastSchema):
    """
    The function adds a new movie cast to the database.
    """
    return MovieController.add_movie_cast(movie_cast.movie_id, movie_cast.actor_id)


@movie_superuser_router.put("/change-movie-title", response_model=MovieSchema,
                            dependencies=[Depends(JWTBearer("super_user"))])
def change_movie_title(movie : MovieSchemaUpdateTitle):
    """
    The function is used to change the title of a movie.
    """
    return MovieController.change_movie_title(movie_id=movie.id, new_movie_title=movie.title)


@movie_superuser_router.put("/change-movie-director", response_model=MovieSchema,
                            dependencies=[Depends(JWTBearer("super_user"))])
def change_movie_director(movie : MovieSchemaUpdateDirector):
    """
    The function allows the user to change the director of a movie.
    """
    return MovieController.change_movie_director(movie_id=movie.id, director=movie.director)


@movie_superuser_router.put("/change-movie-release-year", response_model=MovieSchema,
                            dependencies=[Depends(JWTBearer("super_user"))])
def change_movie_release_year(movie : MovieSchemaUpdateReleaseYear):
    """
    The function updates the release year of a movie.
    """
    return MovieController.change_movie_release_year(movie_id=movie.id, release_year=movie.release_year)


@movie_superuser_router.delete("/delete-movie-genre/", dependencies=[Depends(JWTBearer("super_user"))])
def delete_movie_genre(movie_genre: MovieGenreSchema):
    """
    The function deletes a movie genre from the database.
    """
    return MovieController.delete_movie_genre(movie_id=movie_genre.movie_id, genre_name=movie_genre.genre_name)


@movie_superuser_router.delete("/delete-movie-cast/", dependencies=[Depends(JWTBearer("super_user"))])
def delete_movie_cast_member(movie_cast: MovieCastSchema):
    """
    The function deletes a movie cast member from the database.
    """
    return MovieController.delete_movie_cast(movie_id=movie_cast.movie_id, actor_id=movie_cast.actor_id)


@movie_superuser_router.delete("/delete-movie-by-id/{movie_id}", dependencies=[Depends(JWTBearer("super_user"))])
def delete_movie_by_id(movie_id: int):
    """
    The function deletes a movie from the database by its id.
    """
    return MovieController.delete_movie_by_id(movie_id)
