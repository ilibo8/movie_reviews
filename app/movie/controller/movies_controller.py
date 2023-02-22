"""Module for Movies controller layer"""
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.responses import Response
from app.actor.exceptions import ActorNotFound
from app.genre.exceptions import GenreNotFound
from app.movie.exceptions import MovieNotFound, DuplicateDataEntry, MovieGenreNotFound, MovieCastNotFound
from app.movie.service import MovieService


class MovieController:
    """Class for Movie controller layer methods"""

    @staticmethod
    def add_movie(title, director, release_year, country_of_origin):
        """
        The add_movie function adds a new movie to the database.
        It takes in four arguments: title, director, release_year and country_of_origin.
        The function returns the newly added movie object.
        """
        try:
            movie = MovieService.add_movie(title, director, release_year, country_of_origin)
            return movie
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail="Duplicate data entry. Cannot add that movie.") from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def add_genre_to_movie(movie_id: int, genre_name: str):
        """
        The add_genre_to_movie function adds a genre to a movie.
        It takes in two arguments, the id of the movie and the name of the genre.
        It returns an integer representing success or failure.
        """
        try:
            return MovieService.add_genre_to_movie(movie_id, genre_name)
        except DuplicateDataEntry as err:
            raise HTTPException(status_code=400, detail=err.message) from err
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def add_movie_cast(movie_id: int, actor_id: int):
        """
        The add_movie_cast function adds an actor to a movie's cast.
        It takes two arguments, the id of the movie and the id of the actor.
        If successful, it returns a success message with no content.
        """
        try:
            return MovieService.add_actors_id_to_movie_cast(movie_id, actor_id)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except DuplicateDataEntry as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all():
        """
        The get_all function returns all movies in the database.
        """
        try:
            movies = MovieService.get_all()
            return movies
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def find_movie(movie: dict):
        """
        Function to find movies by multiple criteria.
        """
        try:
            movies = MovieService.find_movie(movie)
            return movies
        except MovieNotFound as err:
            raise HTTPException(status_code=404, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all_movies():
        """
        The get_all_movies function returns all movies in the database.
        """
        try:
            movies = MovieService.get_all_movies()
            return movies
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_movie_by_title(movie_title: str):
        """
        The get_movie_by_title function is used to retrieve a movie by its title.
        It takes in the movie_title as an argument and returns the Movie object if it exists,
        otherwise it raises a HTTPException with status code 404.
        """
        try:
            movie = MovieService.get_movie_by_title(movie_title)
            return movie
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_movies_by_actor_full_name(actor_full_name: str):
        """
        The get_movies_by_actor_full_name function returns a list of movies that an actor has starred in.
        The function takes one parameter, the full name of an actor.
        """
        try:
            movie = MovieService.get_movies_by_actor_full_name(actor_full_name)
            return movie
        except ActorNotFound as err:
            raise HTTPException(status_code=400, detail=err.message) from err
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all_movie_cast():
        """
        The get_all_movie_cast function returns a list of all the movie cast in the database.
        """
        try:
            return MovieService.get_all_movie_cast()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def change_movie_title(movie_id: int, new_movie_title: str):
        """
        The change_movie_title function allows the user to change the title of a movie.
        """
        try:
            return MovieService.change_movie_title(movie_id, new_movie_title)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail="Integrity error. Duplicate data entry.") from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def change_movie_director(movie_id: int, director: str):
        """
        The change_movie_director function is used to change the director of a movie.
        It takes two arguments, movie_id and director. It returns the updated Movie object.
        """
        try:
            return MovieService.change_movie_director(movie_id, director)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail="Integrity error. Duplicate data entry.") from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def change_movie_release_year(movie_id: int, release_year: int):
        """
        The change_movie_release_year function is used to change the release year of a movie.
        """
        try:
            return MovieService.change_movie_release_year(movie_id, release_year)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail="Integrity error. Duplicate data entry.") from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def delete_movie_genre(movie_id: int, genre_name: str):
        """
        The delete_movie_genre function deletes a movie genre from the database.
        It returns a response object with status code 200 if the deletion was successful.
        """
        try:
            if MovieService.delete_movie_genre(movie_id, genre_name):
                return Response(content=f"Genre {genre_name} deleted for movie with id - {movie_id}.", status_code=200)
        except MovieGenreNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except GenreNotFound as err:
            raise HTTPException(status_code=400, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def delete_movie_cast(movie_id: int, actor_id: int):
        """
        The delete_movie_cast function removes an actor from a movie.
        """
        try:
            if MovieService.delete_movie_cast_member(movie_id, actor_id):
                return Response(content=f"Actor with id {actor_id} removed from movie with id {movie_id}.",
                                status_code=200)
        except MovieCastNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def delete_movie_by_id(movie_id: int):
        """
        The delete_movie_by_id function deletes a movie from the database by its id.
        It takes in an integer as an argument, and returns a response object with either
        a success message or error message.
        """
        try:
            if MovieService.delete_movie_by_id(movie_id):
                return Response(content=f"Movie with id {movie_id} deleted.", status_code=200)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err
