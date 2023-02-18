from typing import Type, Union

from app.db import SessionLocal
from app.movie.repository import MovieRepository
from app.reviews.model import Review
from app.reviews.repository import ReviewRepository
from app.reviews.exceptions import ReviewNotFound, Unauthorized, ReviewDuplicateEntry
from app.users.repository import UserRepository


def reformat_output_list(review_list: list) -> list[dict]:
    try:
        with SessionLocal() as db:
            movie_repository = MovieRepository(db)
            user_repository = UserRepository(db)
            reviews_reformatted = []
            for review in review_list:
                movie_title = movie_repository.get_title_by_id(review.movie_id)
                user_name = user_repository.get_user_name_by_user_id(review.user_id)
                reformatted = {"movie_title": movie_title, "user_name": user_name,
                               "rating_number": review.rating_number, "review": review.review}
                reviews_reformatted.append(reformatted)
            return reviews_reformatted
    except Exception as err:
        raise err


def reformat_output_list_with_id(review_list: list) -> list[dict]:
    try:
        with SessionLocal() as db:
            movie_repository = MovieRepository(db)
            user_repository = UserRepository(db)
            reviews_reformatted = []
            for review in review_list:
                movie_title = movie_repository.get_title_by_id(review.movie_id)
                user_name = user_repository.get_user_name_by_user_id(review.user_id)
                reformatted = {"id": review.id, "movie_title": movie_title, "user_name": user_name,
                               "rating_number": review.rating_number, "review": review.review}
                reviews_reformatted.append(reformatted)
            return reviews_reformatted
    except Exception as err:
        raise err


def reformat_output(review: Union[Type[Review], Review]) -> dict:
    try:
        with SessionLocal() as db:
            movie_repository = MovieRepository(db)
            user_repository = UserRepository(db)
            movie_title = movie_repository.get_title_by_id(review.movie_id)
            user_name = user_repository.get_user_name_by_user_id(review.user_id)
            reformatted = {"movie_title": movie_title, "user_name": user_name,
                           "rating_number": review.rating_number, "review": review.review}
            return reformatted
    except Exception as err:
        raise err


class ReviewService:

    @staticmethod
    def add_review(movie_name: str, user_id: int, rating_number: int, review: str):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_name)
                review = review_repository.add_review(movie_id=movie_id, user_id=user_id, rating_number=rating_number,
                                                      review=review)
                return reformat_output(review)
        except ReviewDuplicateEntry as err:
            raise err
        except Exception as err:
            raise err

    @staticmethod
    def get_all_reviews():
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                return review_repository.get_all_reviews()
        except Exception as err:
            raise err

    @staticmethod
    def get_ratings_table():
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                return review_repository.get_ratings_table()
        except Exception as err:
            raise err

    @staticmethod
    def get_average_rating_for_movie(movie_title: str):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_title)
                rating_and_count = review_repository.get_average_rating_and_count_by_movie_id(movie_id)
                return {"movie title": movie_title, "rating": rating_and_count[0], "users rated": rating_and_count[1]}
        except Exception as err:
            raise err

    @staticmethod
    def get_reviews_by_movie_title(movie_title: str):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_title)
                reviews = review_repository.get_reviews_by_movie_id(movie_id)
                if reviews is None:
                    raise ReviewNotFound(f"There is no review with movie id {movie_id}.")
                return reformat_output_list(reviews)
        except Exception as err:
            raise err

    @staticmethod
    def get_reviews_by_user_name(user_name: str):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                user_repository = UserRepository(db)
                user = user_repository.get_user_by_user_name(user_name)
                reviews = review_repository.get_reviews_by_user_id(user.id)
                if reviews is None:
                    raise ReviewNotFound(f"There is no review with user name {user_name}.")
                return reformat_output_list(reviews)
        except Exception as err:
            raise err

    @staticmethod
    def get_personal_reviews(user_id: int):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                reviews = review_repository.get_reviews_by_user_id(user_id)
                if reviews is None:
                    raise ReviewNotFound(f"There are no review.")
                reformatted_reviews = reformat_output_list_with_id(reviews)
                return reformatted_reviews
        except Exception as err:
            raise err

    @staticmethod
    def change_movie_rating_number(movie_name: str, user_id: int, new_rating: int):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_name)
                review = review_repository.change_movie_rating(movie_id, user_id, new_rating)
                return reformat_output(review)
        except Exception as err:
            raise err

    @staticmethod
    def change_movie_review(movie_name: str, user_id: int, new_review: str):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_name)
                review = review_repository.change_movie_review(movie_id, user_id, new_review)
                return reformat_output(review)
        except Exception as err:
            raise err

    @staticmethod
    def delete_review_id_by_user(review_id: int, user_id):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                review = review_repository.delete_review_id_by_user(review_id, user_id)
                if review:
                    return review
        except ReviewNotFound as err:
            raise err
        except Unauthorized as err:
            raise err
        except Exception as err:
            raise err

    @staticmethod
    def delete_review_by_id(review_id: int):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                if review_repository.delete_review_by_id(review_id):
                    return True
        except ReviewNotFound as err:
            raise err
        except Exception as err:
            raise err
