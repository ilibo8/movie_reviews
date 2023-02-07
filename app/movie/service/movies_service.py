from sqlalchemy.exc import IntegrityError
from app.actor.repository import ActorRepository
from app.db.database import SessionLocal
from app.movie.exceptions import MovieNotFoundException
from app.movie.repository import MovieRepository, MovieGenreRepository, MovieCastRepository


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
            except Exception as e:
                raise e

    @staticmethod
    def add_genre_to_movie(movie_id: int, genre_name: str):
        with SessionLocal() as db:
            try:
                movie_genre_repository = MovieGenreRepository(db)
                movie_repo = MovieRepository(db)
                if movie_repo.get_movie_by_id(movie_id) is None:
                    raise MovieNotFoundException(f"No movie with id {movie_id}, first add movie then genre.")
                return movie_genre_repository.add_movie_genre(movie_id, genre_name)
            except Exception as e:
                raise e

    @staticmethod
    def add_actors_id_to_movie_cast(movie_id: int, actors_id: list[int]) -> bool:
        with SessionLocal().begin() as db: #!!!!!!!!!!
            try:

                movie_cast_repository = MovieCastRepository(db)
                movie_repository = MovieRepository(db)
                if movie_repository.get_movie_by_id(movie_id) is None:
                    raise MovieNotFoundException(f"No movie with id {movie_id}, first add movie then actors id.")
                movie_cast_repository.add(movie_id, actors_id)
                return True
            except IntegrityError as e:
                db.rollback()
                db.close()
                raise e

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
                    full_names.sort()
                    movie.genre = genres_names
                    movie.actors = full_names
            return movies
        except Exception as e:
            raise e

    @staticmethod
    def get_movie_by_id(movie_id: int):
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                movie = movie_repository.get_movie_by_id(movie_id)
                if movie is None:
                    raise MovieNotFoundException(f"No movie with id {movie_id} in database.")
                full_names = []
                for item in movie.movie_cast:
                    id = item.actor_id
                    actor_repo = ActorRepository(db)
                    full_names.append(actor_repo.get_actor_full_name_by_id(id)[0])
                genres = movie.movie_genre
                genres_names = []
                for movie_genre in genres:
                    genres_names.append(movie_genre.genre_name)
                full_names.sort()
                movie.genre = genres_names
                movie.actors = full_names
            return movie
        except Exception as e:
            raise e

    @staticmethod
    def get_all_movies_of_certain_genre(genre_name: str) -> list:
        try:
            with SessionLocal() as db:
                movie_genre_repository = MovieGenreRepository(db)
                if len(movie_genre_repository.get_all_movie_ids_of_certain_genre(genre_name)) == 0:
                    raise MovieNotFoundException(f"No movies with genre {genre_name} in database.")
                movie_ids = movie_genre_repository.get_all_movie_ids_of_certain_genre(genre_name)
                movie_repository = MovieRepository(db)
                movie_names = []
                for id in movie_ids:
                    movie_names.append(movie_repository.get_title_by_id(id[0])[0])
                movie_names.sort()
            return movie_names
        except IntegrityError as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def get_movies_by_word_in_title(word: str):
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                return movie_repository.get_movies_by_word_in_title(word)
        except MovieNotFoundException as e:
            raise MovieNotFoundException(e.message)
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
