"""Module for Reviews service"""
from app.db import SessionLocal
from app.movie.repository import MovieRepository
from app.reviews.model import Review
from app.reviews.repository import ReviewRepository
from app.reviews.exceptions import ReviewNotFound, Unauthorized, ReviewDuplicateEntry
from app.users.repository import UserRepository


def reformat_output_list(review_list: list) -> list[dict]:
    """
    The reformat_output_list function takes a list of review objects and reformat them into a list of dictionaries.
    Each dictionary contains the movie title, user_name, rating number and review text for each object in the inputted
    list.
    """
    try:
        with SessionLocal() as dbs:
            movie_repository = MovieRepository(dbs)
            user_repository = UserRepository(dbs)
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
    """
    The reformat_output_list_with_id function takes a list of review objects and reformat them to include the movie
    title and user_name. It returns a list of dictionaries with id, movie_title, user_name, rating_number and review.
    """
    try:
        with SessionLocal() as dbs:
            movie_repository = MovieRepository(dbs)
            user_repository = UserRepository(dbs)
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


def reformat_output(review: Review) -> dict:
    """
    The reformat_output function takes a review object and reformat it into a dictionary.
    It returns the movie title, user_name, rating number and review text as key value pairs.
    """
    try:
        with SessionLocal() as dbs:
            movie_repository = MovieRepository(dbs)
            user_repository = UserRepository(dbs)
            movie_title = movie_repository.get_title_by_id(review.movie_id)
            user_name = user_repository.get_user_name_by_user_id(review.user_id)
            reformatted = {"movie_title": movie_title, "user_name": user_name,
                           "rating_number": review.rating_number, "review": review.review}
            return reformatted
    except Exception as err:
        raise err


class ReviewService:
    """Class for Review service layer"""

    @staticmethod
    def add_review(movie_name: str, user_id: int, rating_number: int, review: str):
        """
        The add_review function adds a review to the database.
        rating number is an integer between 1 and 10 inclusive which represents how much you liked/disliked this
        particular movie out of ten (10 being most liked).
        review is a string containing your opinion about this particular film.
        """
        try:
            with SessionLocal() as dbs:
                review_repository = ReviewRepository(dbs)
                movie_repository = MovieRepository(dbs)
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
        """
        The get_all_reviews function returns all reviews in the database.
        """
        try:
            with SessionLocal() as dbs:
                review_repository = ReviewRepository(dbs)
                return review_repository.get_all_reviews()
        except Exception as err:
            raise err

    @staticmethod
    def get_ratings_table():
        """
        The get_ratings_table function returns a table of ratings for all the reviews in the database.
        The table is sorted by review date, with most recent reviews first.
        """
        try:
            with SessionLocal() as dbs:
                review_repository = ReviewRepository(dbs)
                return review_repository.get_ratings_table()
        except Exception as err:
            raise err

    @staticmethod
    def get_average_rating_for_movie(movie_title: str):
        """
        The get_average_rating_for_movie function takes a movie title as an argument and returns the average
        rating for that movie. It first retrieves the Movie ID from the database using get_movie_id_by_title,
        then uses get_average_rating to retrieve the average rating and number of ratings for that movie.
        """
        try:
            with SessionLocal() as dbs:
                review_repository = ReviewRepository(dbs)
                movie_repository = MovieRepository(dbs)
                movie_id = movie_repository.get_movie_id_by_title(movie_title)
                rating_and_count = review_repository.get_average_rating_and_count_by_movie_id(movie_id)
                return {"movie title": movie_title, "rating": rating_and_count[0], "users rated": rating_and_count[1]}
        except Exception as err:
            raise err

    @staticmethod
    def get_reviews_by_movie_title(movie_title: str):
        """
        The get_reviews_by_movie_title function takes a movie title as an argument and returns all the reviews for
        that movie. If there are no reviews for that movie, it will return an error message.
        """
        try:
            with SessionLocal() as dbs:
                review_repository = ReviewRepository(dbs)
                movie_repository = MovieRepository(dbs)
                movie_id = movie_repository.get_movie_id_by_title(movie_title)
                reviews = review_repository.get_reviews_by_movie_id(movie_id)
                if reviews is None:
                    raise ReviewNotFound(f"There is no review with movie id {movie_id}.")
                return reformat_output_list(reviews)
        except Exception as err:
            raise err

    @staticmethod
    def get_reviews_by_user_name(user_name: str):
        """
        The get_reviews_by_user_name function takes a user_name as an argument and returns all the reviews
        written by that user. If no review is found, it raises a ReviewNotFound exception.
        """
        try:
            with SessionLocal() as dbs:
                review_repository = ReviewRepository(dbs)
                user_repository = UserRepository(dbs)
                user = user_repository.get_user_by_user_name(user_name)
                reviews = review_repository.get_reviews_by_user_id(user.id)
                if reviews is None:
                    raise ReviewNotFound(f"There is no review with user name {user_name}.")
                return reformat_output_list(reviews)
        except Exception as err:
            raise err

    @staticmethod
    def get_personal_reviews(user_id: int):
        """
        The get_personal_reviews function retrieves all the reviews that a user has created.
        It takes in an integer as input and returns a list of dictionaries, where each dictionary contains
        information about one review.
        """
        try:
            with SessionLocal() as dbs:
                review_repository = ReviewRepository(dbs)
                reviews = review_repository.get_reviews_by_user_id(user_id)
                if reviews is None:
                    raise ReviewNotFound("There are no review.")
                reformatted_reviews = reformat_output_list_with_id(reviews)
                return reformatted_reviews
        except Exception as err:
            raise err

    @staticmethod
    def change_movie_rating_number(movie_name: str, user_id: int, new_rating: int):
        """
        The change_movie_rating_number function allows a user to change the rating of a movie they have previously
        rated.
        """
        try:
            with SessionLocal() as dbs:
                review_repository = ReviewRepository(dbs)
                movie_repository = MovieRepository(dbs)
                movie_id = movie_repository.get_movie_id_by_title(movie_name)
                review = review_repository.change_movie_rating(movie_id, user_id, new_rating)
                return reformat_output(review)
        except Exception as err:
            raise err

    @staticmethod
    def change_movie_review(movie_name: str, user_id: int, new_review: str):
        """
        The change_movie_review function allows a user to change the review they have written for a movie.
        """
        try:
            with SessionLocal() as dbs:
                review_repository = ReviewRepository(dbs)
                movie_repository = MovieRepository(dbs)
                movie_id = movie_repository.get_movie_id_by_title(movie_name)
                review = review_repository.change_movie_review(movie_id, user_id, new_review)
                return reformat_output(review)
        except Exception as err:
            raise err

    @staticmethod
    def delete_review_id_by_user(review_id: int, user_id):
        """
        The delete_review_id_by_user function deletes a review by the user's id.
        """
        try:
            with SessionLocal() as dbs:
                review_repository = ReviewRepository(dbs)
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
        """
        The delete_review_by_id function deletes a review from the database by its id.
        It takes in an integer as an argument and returns True if it is successful.
        """
        try:
            with SessionLocal() as dbs:
                review_repository = ReviewRepository(dbs)
                if review_repository.delete_review_by_id(review_id):
                    return True
        except ReviewNotFound as err:
            raise err
        except Exception as err:
            raise err
