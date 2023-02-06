from fastapi import HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.exc import IntegrityError

from app.movie.exceptions import MovieNotFoundException
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
    def get_all_movies():
        try:
            movies = MovieService.get_all_movies()
            return movies
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_genre_of_movie(movie_id: int):
        try:
            movie_genres = MovieService.get_genre_of_movie(movie_id)
            return movie_genres
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))



    @staticmethod
    def delete_movie_genre(movie_id: int, genre_name: str):
        try:
            if MovieService.delete_movie_genre(movie_id, genre_name):
                return Response(content=f"Genre {genre_name}deleted for movie with id - {movie_id} ", status_code=200)
        except MovieNotFoundException as e:
            raise HTTPException(status_code=400, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
