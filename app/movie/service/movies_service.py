from sqlalchemy.exc import IntegrityError

from app.actor.repository import ActorRepository
from app.db.database import SessionLocal
from app.movie.exceptions import MovieNotFoundException
from app.movie.repository import MovieRepository, MovieGenreRepository


class MovieService:

    @staticmethod
    def add_movie(title, director, release_year, country_of_origin):
        with SessionLocal() as db:
            try:
                movie_repository = MovieRepository(db)
                return movie_repository.add_movie \
                    (title=title, director=director, release_year=release_year, country_of_origin=country_of_origin)
            except IntegrityError:
                raise IntegrityError

    @staticmethod
    def get_all_movies() -> list:
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                movies = movie_repository.get_all_movies()
                for movie in movies:
                    movie_cast_pair = movie.movie_cast
                    full_names = []
                    for item in movie_cast_pair:
                        id = item.actor_id
                        actor_repo = ActorRepository(db)
                        full_names.append(actor_repo.get_actor_full_name_by_id(id)[0])
                    genres = movie.movie_genre
                    genres_names = []
                    for movie_genre in genres:
                        genres_names.append(movie_genre.genre_name)
                    movie.genre = genres_names
                    movie.actors = full_names
            return movies
        except Exception as e:
            raise e

    @staticmethod
    def get_genre_of_movie(movie_id: int):
        try:
            with SessionLocal() as db:
                movie_genre_repository = MovieGenreRepository(db)
                return movie_genre_repository.get_genres_of_movie(movie_id)
        except Exception as e:
            raise e

    @staticmethod
    def delete_movie_genre(movie_id: int, genre_name: str):
        try:
            with SessionLocal() as db:
                movie_genre_repository = MovieGenreRepository(db)
                if movie_genre_repository.delete_movie_genre(movie_id, genre_name):
                    return True
                raise MovieNotFoundException(f"There is no movie with id {movie_id} and genre {genre_name}")
        except MovieNotFoundException as e:
            raise MovieNotFoundException(e.message)
        except Exception as e:
            raise e
