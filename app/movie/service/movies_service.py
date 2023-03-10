"""Module for Movie service layer"""
from typing import Type
from sqlalchemy.exc import IntegrityError
from app.actor.exceptions import ActorNotFound
from app.actor.repository import ActorRepository
from app.db import SessionLocal
from app.genre.exceptions import GenreNotFound
from app.genre.repository import GenreRepository
from app.movie.exceptions import MovieNotFound, MovieGenreNotFound, MovieCastNotFound
from app.movie.model import Movie
from app.movie.repository import MovieRepository, MovieGenreRepository, MovieCastRepository


class MovieService:
    """Class for Movie service layer methods"""

    @staticmethod
    def add_movie(title, director, release_year, country_of_origin):
        """
        The add_movie function adds a new movie to the database.
        The function returns the id of the newly added movie.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                return movie_repository.add_movie(title, director, release_year, country_of_origin)
        except Exception as err:
            raise err

    @staticmethod
    def add_genre_to_movie(movie_id: int, genre_name: str):
        """
        The add_genre_to_movie function adds a genre to a movie.
        If there is no such movie or if there is no such genre it will raise an error.
        """
        try:
            with SessionLocal() as db:
                movie_genre_repository = MovieGenreRepository(db)
                movie_repository = MovieRepository(db)
                genre_repository = GenreRepository(db)
                if movie_repository.get_movie_by_id(movie_id) is None:
                    raise MovieNotFound(f"No movie with id {movie_id}, first add movie then genre.")
                if not genre_repository.check_is_there(genre_name):
                    raise MovieNotFound(f"No genre {genre_name}, add to genre list first.")
                return movie_genre_repository.add_movie_genre(movie_id, genre_name)
        except Exception as err:
            raise err

    @staticmethod
    def add_actors_id_to_movie_cast(movie_id: int, actor_id: int):
        """
        The add_actors_id_to_movie_cast function adds an actor to a movie cast.
        If either one doesn't exist it raises MovieNotFound exception.
        """
        try:
            with SessionLocal() as db:
                movie_cast_repository = MovieCastRepository(db)
                movie_repository = MovieRepository(db)
                actor_repository = ActorRepository(db)
                if movie_repository.get_movie_by_id(movie_id) is None:
                    raise MovieNotFound(f"No movie with id {movie_id}, first add movie then movie cast.")
                if actor_repository.get_actor_by_id(actor_id) is None:
                    raise MovieNotFound(f"Actor id {actor_id} doesn't exist.")
                movie_cast = movie_cast_repository.add(movie_id, actor_id)
                return movie_cast
        except Exception as err:
            raise err

    @staticmethod
    def get_all() -> list[Type[Movie]]:
        """
        The get_all function returns all movies in the database.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                movies = movie_repository.get_all_movies()
                return movies
        except Exception as err:
            raise err

    @staticmethod
    def get_all_movies() -> list:
        """
        The get_all_movies function returns a list of all movies in the database.
        The function will return an empty list if there are no movies in the database.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                movies = movie_repository.get_all_movies_order_by_name()
                for movie in movies:
                    movie_cast_pair = movie.movie_cast
                    full_names = []
                    for item in movie_cast_pair:
                        actor_id = item.actor_id
                        actor_repo = ActorRepository(db)
                        full_names.append(actor_repo.get_actor_full_name_by_id(actor_id))
                    genres = movie.movie_genre
                    genres_names = []
                    for movie_genre in genres:
                        genres_names.append(movie_genre.genre_name)
                    full_names.sort()
                    movie.genre = genres_names
                    movie.actors = full_names
                return movies
        except Exception as err:
            raise err

    @staticmethod
    def get_movie_by_title(movie_title: str):
        """
        The get_movie_by_title function takes a movie title as an argument and returns the full details of that movie.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                movie = movie_repository.get_movie_by_title(movie_title)
                if movie is None:
                    raise MovieNotFound(f"No movie with title {movie_title} in database.")
                full_names = []
                for item in movie.movie_cast:
                    actor_id = item.actor_id
                    actor_repo = ActorRepository(db)
                    full_names.append(actor_repo.get_actor_full_name_by_id(actor_id))
                genres = movie.movie_genre
                genres_names = []
                for movie_genre in genres:
                    genres_names.append(movie_genre.genre_name)
                full_names.sort()
                movie.genre = genres_names
                movie.actors = full_names
                return movie
        except Exception as err:
            raise err

    @staticmethod
    def get_movies_by_actor_full_name(actor_full_name: str):
        """
        The function takes an actor's full name as a string and returns all movies that
        the actor has been in.
        """
        try:
            with SessionLocal() as db:
                movie_repo = MovieRepository(db)
                actor_repo = ActorRepository(db)
                movie_cast_repo = MovieCastRepository(db)
                actor = actor_repo.get_actor_by_full_name(actor_full_name)
                if actor is None:
                    raise ActorNotFound("There is no actor with that name and last name.")
                movie_ids = movie_cast_repo.get_movie_ids_by_actor_id(actor.id)
                if len(movie_ids) == 0:
                    raise MovieNotFound(f"No movies in database for actor id {actor.id}")
                all_movies = [movie_repo.get_movie_by_id(id) for id in movie_ids]
                for movie in all_movies:
                    full_names = []
                    for item in movie.movie_cast:
                        actor_id = item.actor_id
                        actor_repo = ActorRepository(db)
                        full_names.append(actor_repo.get_actor_full_name_by_id(actor_id))
                    genres = movie.movie_genre
                    genres_names = []
                    for movie_genre in genres:
                        genres_names.append(movie_genre.genre_name)
                    full_names.sort()
                    movie.genre = genres_names
                    movie.actors = full_names
                all_movies.sort(key=lambda x : x.title)
                return all_movies
        except Exception as err:
            raise err

    @staticmethod
    def get_all_movie_cast():
        """
        The function returns all the movie cast in the database.
        """
        try:
            with SessionLocal() as db:
                movie_cast_repository = MovieCastRepository(db)
                movie_repository = MovieRepository(db)
                actor_repository = ActorRepository(db)
                movie_cast = movie_cast_repository.get_all()
                all_cast = []
                for cast in movie_cast:
                    movie_name = movie_repository.get_title_by_id(cast.movie_id)
                    actor_name = actor_repository.get_actor_full_name_by_id(cast.actor_id)
                    all_cast.append({"movie_id": cast.movie_id, "movie_name": movie_name, "actor_id": cast.actor_id,
                                     "actor_name": actor_name})
                return all_cast
        except Exception as err:
            raise err

    @staticmethod
    def find_movie(movie: dict):
        """
        Returns movies based on provided criteria.
        """
        try:
            with SessionLocal() as db:
                movie_cast_repository = MovieCastRepository(db)
                movie_repository = MovieRepository(db)
                genre_repository = GenreRepository(db)
                movie_genre_repository = MovieGenreRepository(db)
                actor_repository = ActorRepository(db)
                test_list = []
                if movie["word_in_title"] is not None:
                    movie_titles = movie_repository.get_movies_by_word_in_title(movie.get("word_in_title"))
                    if len(movie_titles) != 0:
                        movie_title_ids = [movie.id for movie in movie_titles]
                        test_list.append(set(movie_title_ids))
                    else:
                        raise MovieNotFound(f"There is no data for title {movie.get('word_in_title')}")
                if movie["director"] is not None:
                    movie_directors = movie_repository.get_movies_by_director(movie.get("director"))
                    if len(movie_directors) != 0:
                        movie_directors_ids = [movie.id for movie in movie_directors]
                        test_list.append(set(movie_directors_ids))
                    else:
                        raise MovieNotFound(f"There is no data for query director {movie.get('director')}")
                if movie["release_year"] is not None:
                    movie_years = movie_repository.get_movies_by_release_year(movie.get("release_year"))
                    if len(movie_years) != 0:
                        movie_years_ids = [movie.id for movie in movie_years]
                        test_list.append(set(movie_years_ids))
                    else:
                        raise MovieNotFound(f"There is no data for query release year {movie.get('release_year')}")
                if movie["genre"] is not None:
                    if genre_repository.check_is_there(movie["genre"]):
                        movie_genre = movie_genre_repository.get_all_movies_of_certain_genre(movie.get("genre"))
                        if len(movie_genre) != 0:
                            movie_genre_ids = [movie.movie_id for movie in movie_genre]
                            test_list.append(set(movie_genre_ids))
                        else:
                            raise MovieNotFound(f"There is no data for query genre {movie.get('genre')}")
                    else:
                        raise MovieNotFound(f"There is no data for query genre {movie.get('genre')}")
                if movie["country_of_origin"] is not None:
                    movies_country_of_origin = movie_repository.get_movies_by_country_of_origin \
                        (movie.get("country_of_origin"))
                    if len(movies_country_of_origin) != 0:
                        movies_country_of_origin_ids = [movie.id for movie in movies_country_of_origin]
                        test_list.append(set(movies_country_of_origin_ids))
                    else:
                        raise MovieNotFound(f"There is no data for query country of origin "
                                            f"{movie.get('country_of_origin')}")
                if movie["actor"] is not None:
                    actor = actor_repository.get_actor_by_full_name(movie.get("actor"))
                    if actor is not None:
                        movie_cast = movie_cast_repository.get_movies_by_actor_id(actor.id)
                        if len(movie_cast) != 0:
                            movie_actor_ids = [movie.movie_id for movie in movie_cast]
                            test_list.append(set(movie_actor_ids))
                        else:
                            raise MovieNotFound(f"There is no data for query actor {movie.get('actor')}")
                    else:
                        raise MovieNotFound(f"There is no data for query actor {movie.get('actor')}")
                if len(test_list) == 0:
                    raise MovieNotFound("There is no data that matches this query.")
                movie_ids = set.intersection(*test_list)
                if len(movie_ids) == 0:
                    raise MovieNotFound("There is no data that matches this query.")
                movies = [movie_repository.get_movie_by_id(x) for x in movie_ids]
                for movie in movies:
                    full_names = []
                    for item in movie.movie_cast:
                        actor_id = item.actor_id
                        actor_repo = ActorRepository(db)
                        full_names.append(actor_repo.get_actor_full_name_by_id(actor_id))
                    genres = movie.movie_genre
                    genres_names = []
                    for movie_genre in genres:
                        genres_names.append(movie_genre.genre_name)
                    full_names.sort()
                    movie.genre = genres_names
                    movie.actors = full_names
                movies.sort(key=lambda x: x.title)
                return movies
        except Exception as err:
            raise err

    @staticmethod
    def change_movie_title(movie_id: int, new_movie_title: str):
        """
        The change_movie_title function allows the user to change the title of a movie.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                movies = movie_repository.change_movie_title(movie_id, new_movie_title)
                return movies
        except MovieNotFound as err:
            raise err
        except IntegrityError as err:
            raise err
        except Exception as err:
            raise err

    @staticmethod
    def change_movie_director(movie_id: int, director: str):
        """
        The change_movie_director function allows the user to change the director of a movie.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                movies = movie_repository.change_movie_director(movie_id, director)
                return movies
        except MovieNotFound as err:
            raise err
        except IntegrityError as err:
            raise err
        except Exception as err:
            raise err

    @staticmethod
    def change_movie_release_year(movie_id: int, release_year: int):
        """
        The change_movie_release_year function is used to change the release year of a movie.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                movies = movie_repository.change_movie_release_year(movie_id, release_year)
                return movies
        except MovieNotFound as err:
            raise err
        except IntegrityError as err:
            raise err
        except Exception as err:
            raise err

    @staticmethod
    def delete_movie_genre(movie_id: int, genre_name: str):
        """
        The delete_movie_genre function deletes a movie genre object from the database.
        It takes two arguments, movie_id and genre_name. It returns True if it is successful.
        """
        try:
            with SessionLocal() as db:
                movie_genre_repository = MovieGenreRepository(db)
                movie_repository = MovieRepository(db)
                genre_repository = GenreRepository(db)
                if movie_repository.get_movie_by_id(movie_id) is None:
                    raise MovieNotFound(f"There is no movie with id {movie_id}")
                if genre_repository.check_is_there(genre_name) is False:
                    raise GenreNotFound(f"There is no genre name {genre_name}")
                if movie_genre_repository.delete_movie_genre(movie_id, genre_name) is None:
                    raise MovieGenreNotFound
                return True
        except MovieGenreNotFound as err:
            raise err
        except Exception as err:
            raise err

    @staticmethod
    def delete_movie_cast_member(movie_id: int, actor_id: int):
        """
        Delete movie cast member by movie_id and actor_id
        """
        try:
            with SessionLocal() as db:
                movie_cast_repository = MovieCastRepository(db)
                movie_repository = MovieRepository(db)
                actor_repository = ActorRepository(db)
                if movie_repository.get_movie_by_id(movie_id) is None:
                    raise MovieNotFound(f"There is no movie with id {movie_id}")
                if actor_repository.get_actor_by_id(actor_id) is None:
                    raise ActorNotFound(f"There is no actor with id {actor_id}")
                if movie_cast_repository.delete_movie_cast(movie_id, actor_id) is None:
                    raise MovieCastNotFound
                return True
        except MovieCastNotFound as err:
            raise err
        except Exception as err:
            raise err

    @staticmethod
    def delete_movie_by_id(movie_id: int):
        """
        Delete movie by id, if id not fount raise MovieNotFound exception
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                if movie_repository.delete_movie_by_id(movie_id) is None:
                    raise MovieNotFound(f"There is no movie with id {movie_id}.")
                return True
        except MovieNotFound as err:
            raise err
        except Exception as err:
            raise err
