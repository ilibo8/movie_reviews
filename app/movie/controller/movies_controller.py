from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.movie.service import MovieService


class MovieController:

    @staticmethod
    def add_movie(title, director, release_year, country_of_origin):
        try:
            movie = MovieService.add_movie(title, director, release_year, country_of_origin)
            return movie
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e))
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
    def get_all_movies():
        movies = MovieService.get_all_movies()
        return movies
