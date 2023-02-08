from fastapi import HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.exc import IntegrityError

from app.genre.exceptions import GenreNotFoundException
from app.movie.exceptions import NotFoundException, DuplicateDataEntryException
from app.movie.service import MovieService


class MovieController:

    @staticmethod
    def add_movie(title, director, release_year, country_of_origin):
        try:
            movie = MovieService.add_movie(title, director, release_year, country_of_origin)
            return movie
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Integrity error. Cannot add that movie.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def add_genre_to_movie(movie_id: int, genre_name: str):
        try:
            return MovieService.add_genre_to_movie(movie_id, genre_name)
        except DuplicateDataEntryException as e:
            raise HTTPException(status_code=400, detail=e.message)
        except NotFoundException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def add_movie_cast(movie_id: int, actor_id: int):
        try:
            return MovieService.add_actors_id_to_movie_cast(movie_id, actor_id)
        except NotFoundException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except DuplicateDataEntryException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_movies():
        try:
            movies = MovieService.get_all_movies()
            return movies
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_movie_by_id(movie_id: int):
        try:
            movie = MovieService.get_movie_by_id(movie_id)
            return movie
        except NotFoundException as e:
            raise HTTPException(status_code=e.code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_movies_of_certain_genre(genre_name: str):
        try:
            return MovieService.get_all_movies_of_certain_genre(genre_name)
        except GenreNotFoundException as e:
            raise HTTPException(status_code=400, detail=e.message)
        except NotFoundException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_movies_by_word_in_title(word: str):
        try:
            movie = MovieService.get_movies_by_word_in_title(word)
            return movie
        except NotFoundException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_movie_genre(movie_id: int, genre_name: str):
        try:
            if MovieService.delete_movie_genre(movie_id, genre_name):
                return Response(content=f"Genre {genre_name}deleted for movie with id - {movie_id} ", status_code=200)
        except NotFoundException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
