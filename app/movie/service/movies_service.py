from sqlalchemy.exc import IntegrityError
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
                return movies
            #     movies_with_cast_and_genre = []
            #     for movie in movies:
            #         movie.actors = []
            #         movie.genres = []
            #         movie_cast_repo = MovieCastRepository(db)
            #         cast_ids = movie_cast_repo.get_cast_ids_by_movie_id(movie.id)
            #         for id in cast_ids:
            #             actor_repo = ActorRepository(db)
            #             actor = actor_repo.find_actor_name_by_id(id[0])
            #             movie.actors.append(actor.full_name)
            #         movie_genre_repo = MovieGenreRepository(db)
            #         movie_genres = movie_genre_repo.get_genres_of_movie(movie.id)
            #         movie.genres.append([genre[0] for genre in movie_genres])
            #         movies_with_cast_and_genre.append(movie)
            # return movies_with_cast_and_genre
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
