from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError
from starlette.responses import Response

from app.actor.exceptions import ActorNotFound
from app.genre.exceptions import GenreNotFound
from app.movie.exceptions import MovieNotFound, DuplicateDataEntry, MovieGenreNotFound, MovieCastNotFound
from app.movie.service import MovieService


class MovieController:

    @staticmethod
    def add_movie(title, director, release_year, country_of_origin):
        try:
            movie = MovieService.add_movie(title, director, release_year, country_of_origin)
            return movie
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Duplicate data entry. Cannot add that movie.")
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def add_genre_to_movie(movie_id: int, genre_name: str):
        try:
            return MovieService.add_genre_to_movie(movie_id, genre_name)
        except DuplicateDataEntry as err:
            raise HTTPException(status_code=400, detail=err.message)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def add_movie_cast(movie_id: int, actor_id: int):
        try:
            return MovieService.add_actors_id_to_movie_cast(movie_id, actor_id)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except DuplicateDataEntry as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all():
        try:
            movies = MovieService.get_all()
            return movies
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all_movies():
        try:
            movies = MovieService.get_all_movies()
            return movies
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_movie_by_title(movie_title: str):
        try:
            movie = MovieService.get_movie_by_title(movie_title)
            return movie
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_movies_of_certain_genre(genre_name: str):
        try:
            return MovieService.get_all_movies_of_certain_genre(genre_name)
        except GenreNotFound as err:
            raise HTTPException(status_code=400, detail=err.message)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_movies_by_word_in_title(word: str):
        try:
            movie = MovieService.get_movies_by_word_in_title(word)
            return movie
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_movies_by_actor_full_name(actor_full_name: str):
        try:
            movie = MovieService.get_movies_by_actor_full_name(actor_full_name)
            return movie
        except ActorNotFound as err:
            raise HTTPException(status_code=400, detail=err.message)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all_movies_by_director(director_name: str):
        try:
            movies = MovieService.get_all_movies_by_director(director_name)
            return movies
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all_directors():
        try:
            return MovieService.get_all_directors()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def delete_movie_genre(movie_id: int, genre_name: str):
        try:
            if MovieService.delete_movie_genre(movie_id, genre_name):
                return Response(content=f"Genre {genre_name} deleted for movie with id - {movie_id}.", status_code=200)
        except MovieGenreNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except GenreNotFound as err:
            raise HTTPException(status_code=400, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def delete_movie_cast(movie_id: int, actor_id: int):
        try:
            if MovieService.delete_movie_cast_member(movie_id, actor_id):
                return Response(content=f"Actor with id {actor_id} removed from movie with id {movie_id}.",
                                status_code=200)
        except MovieCastNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def delete_movie_by_id(movie_id: int):
        try:
            if MovieService.delete_movie_by_id(movie_id):
                return Response(content=f"Movie with id {movie_id} deleted.", status_code=200)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
