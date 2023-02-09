from app.actor.repository import ActorRepository
from app.db import SessionLocal
from app.genre.exceptions import GenreNotFoundException
from app.genre.repository import GenreRepository
from app.movie.exceptions import NotFoundException
from app.movie.repository import MovieRepository, MovieGenreRepository, MovieCastRepository


class MovieService:

    @staticmethod
    def add_movie(title, director, release_year, country_of_origin):
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                return movie_repository.add_movie \
                    (title=title, director=director, release_year=release_year, country_of_origin=country_of_origin)
        except Exception as e:
            raise e

    @staticmethod
    def add_genre_to_movie(movie_id: int, genre_name: str):
        try:
            with SessionLocal() as db:
                movie_genre_repository = MovieGenreRepository(db)
                movie_repository = MovieRepository(db)
                genre_repository = GenreRepository(db)
                if movie_repository.get_movie_by_id(movie_id) is None:
                    raise NotFoundException(f"No movie with id {movie_id}, first add movie then genre.")
                if not genre_repository.check_is_there(genre_name):
                    raise NotFoundException(f"No genre {genre_name}, add to genre list first.")
                return movie_genre_repository.add_movie_genre(movie_id, genre_name)
        except Exception as e:
            raise e

    @staticmethod
    def add_actors_id_to_movie_cast(movie_id: int, actor_id: int):
        try:
            with SessionLocal() as db:
                movie_cast_repository = MovieCastRepository(db)
                movie_repository = MovieRepository(db)
                actor_repository = ActorRepository(db)
                if movie_repository.get_movie_by_id(movie_id) is None:
                    raise NotFoundException(f"No movie with id {movie_id}, first add movie then movie cast.")
                # if actor_repository.find_actor_by_id(actor_id) is None:
                #     raise NotFoundException(f"Actor id {actor_id} doesn't exist.")
                movie_cast = movie_cast_repository.add(movie_id, actor_id)
                return movie_cast
        except Exception as e:
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
                    raise NotFoundException(f"No movie with id {movie_id} in database.")
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
                genre_repository = GenreRepository(db)
                if not genre_repository.check_is_there(genre_name):
                    raise GenreNotFoundException(f"Wrong input. No genre {genre_name}.")
                if len(movie_genre_repository.get_all_movie_ids_of_certain_genre(genre_name)) == 0:
                    raise NotFoundException(f"No movies with genre {genre_name} in database.")
                movie_ids = movie_genre_repository.get_all_movie_ids_of_certain_genre(genre_name)
                movie_repository = MovieRepository(db)
                movie_names = []
                for id in movie_ids:
                    movie_names.append(movie_repository.get_title_by_id(id[0])[0])
                movie_names.sort()
            return movie_names
        except Exception as e:
            raise e

    @staticmethod
    def get_movies_by_word_in_title(word: str):
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                movies = movie_repository.get_movies_by_word_in_title(word)
                if len(movies) == 0:
                    raise NotFoundException(f"There are no movies with {word} in title.")
                for movie in movies:
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
                return movies
        except Exception as e:
            raise e

    @staticmethod
    def get_movies_by_actor_id(actor_id: int):
        try:
            with SessionLocal() as db:
                movie_repo = MovieRepository(db)
                movie_cast_repo = MovieCastRepository(db)
                movie_ids = movie_cast_repo.get_movie_ids_by_actor_id(actor_id)
                if len(movie_ids) == 0:
                    raise NotFoundException(f"No movies in database for actor id {actor_id}")
                movies_names = []
                for id in movie_ids:
                    movie = movie_repo.get_title_by_id(id[0])[0]
                    movies_names.append(movie)
                return movies_names
        except Exception as e:
            raise e

    @staticmethod
    def get_all_directors():
        try:
            with SessionLocal() as db:

                movie_repository = MovieRepository(db)
                directors = movie_repository.get_all_directors()
                directors_names = [person[0] for person in directors]
                directors_names.sort()
                return directors_names
        except Exception as e:
            raise e

    @staticmethod
    def get_all_movies_by_director(director_name: str):
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                movies = movie_repository.get_movies_by_director(director_name)
                return movies
        except Exception as e:
            raise e

    @staticmethod
    def delete_movie_genre(movie_id: int, genre_name: str):
        try:
            with SessionLocal() as db:
                movie_genre_repository = MovieGenreRepository(db)
                if movie_genre_repository.delete_movie_genre(movie_id, genre_name):
                    return True
                raise NotFoundException(f"There is no movie with id {movie_id} and genre {genre_name}")
        except NotFoundException as e:
            raise NotFoundException(e.message)
        except Exception as e:
            raise e
