"""Module for Reviews controller"""
from fastapi import HTTPException, Response
from sqlalchemy.exc import IntegrityError

from app.genre.exceptions import GenreNotFound
from app.movie.exceptions import MovieNotFound
from app.reviews.exceptions import ReviewNotFound, ReviewDuplicateEntry, Unauthorized
from app.reviews.service import ReviewService
from app.users.exceptions import UserNotFound


class ReviewController:
    """Class for Review controller methods"""

    @staticmethod
    def add_review(movie_name: str, user_id: int, rating_number: int, review: str):
        """
        The add_review function adds a review to the database.
        It takes in movie_name, user_id, rating_number and review as parameters.
        It returns the id of the newly created review.
        """
        try:
            return ReviewService.add_review(movie_name, user_id, rating_number, review)
        except ReviewDuplicateEntry as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all_reviews():
        """
        The get_all_reviews function returns all reviews in the database.
        """
        try:
            return ReviewService.get_all_reviews()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_average_rating_and_count_for_all_movies():
        """
        Returns average rating and number of user rating movie.
        """
        try:
            return ReviewService.get_average_rating_and_count_for_all_movies()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_average_rating_and_count_for_movie(movie_title: str):
        """
        The get_average_rating_for_movie function accepts a movie title as an argument and returns the average
        rating for that movie. If no ratings are found, it raises a MovieNotFound exception.
        """
        try:
            return ReviewService.get_average_rating_for_movie(movie_title)
        except ReviewNotFound as err:
            raise HTTPException(status_code=404, detail=str(err)) from err
        except MovieNotFound as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_reviews_by_movie_title(movie_title: str):
        """
        The get_reviews_by_movie_title function returns a list of reviews for the movie with the given title.
        If no such movie exists, it raises a MovieNotFound exception.
        If no review exists for that movie, it raises a ReviewNotFound exception.
        """
        try:
            return ReviewService.get_reviews_by_movie_title(movie_title)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except ReviewNotFound as err:
            raise HTTPException(status_code=404, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_reviews_by_user_name(user_name: str):
        """
        The get_reviews_by_user_name function is used to retrieve all reviews by a specific user.
        It takes in the user_name as an argument and returns a list of review objects.
        """
        try:
            return ReviewService.get_reviews_by_user_name(user_name)
        except UserNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except ReviewNotFound as err:
            raise HTTPException(status_code=404, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_personal_reviews(user_id: int):
        """
        The get_personal_reviews function is used to retrieve all the reviews that a user has made.
        It takes in an integer representing the user id and returns a list of dictionaries containing
        the review information for each review that was made by this particular user.
        """
        try:
            return ReviewService.get_personal_reviews(user_id)
        except UserNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except ReviewNotFound as err:
            raise HTTPException(status_code=404, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_top_five_users_with_most_reviews():
        """
        Get list of most active users with number of their reviews.
        """
        try:
            return ReviewService.get_top_five_users_with_most_reviews()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_top_n_movies_by_avg_rating(top: int):
        """
        Get list of top n movies by average rating
        """
        try:
            return ReviewService.get_top_n_movies_by_avg_rating(top)
        except ValueError as err:
            raise HTTPException(status_code=404, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_five_best_rated_movies_by_genre(genre: str):
        """
        Returns top n movies of certain genre by their average rating. Returns list[(movie_id, avg_rating, user_rated)]
        """
        try:
            return ReviewService.get_five_best_rated_movies_by_genre(genre)
        except GenreNotFound as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def change_movie_rating_number(movie_name: str, user_id: int, new_rating: int):
        """
        The change_movie_rating_number function is used to change the rating number of a movie.
        It takes in three parameters: movie_name, user_id and new_rating. It returns a dictionary with two keys:
        movie_name and user_id;. The value for each key is the corresponding parameter passed into the function.
        """
        try:
            return ReviewService.change_movie_rating_number(movie_name, user_id, new_rating)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def change_movie_review(movie_name: str, user_id: int, new_review: str):
        """
        The change_movie_review function allows a user to change the review they have written for a movie.
        It takes in three parameters: movie_name, user_id and new_review. It then calls the change_movie_review
        function from ReviewService which returns True or False depending on whether it was successful.
        """
        try:
            return ReviewService.change_movie_review(movie_name, user_id, new_review)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def delete_review_id_by_user(review_id: int, user_id):
        """
        The delete_review_id_by_user function deletes a review from the database.
        It takes in two parameters, review_id and user_id. It then checks if the user is authorized to delete this
        specific review by comparing their id's. If they are authorized it then proceeds to delete the specified review
        from the database.
        """
        try:
            if ReviewService.delete_review_id_by_user(review_id, user_id):
                return Response(content=f"Review with id {review_id} is deleted", status_code=200)
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Unauthorized as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def delete_review_by_id(review_id: int):
        """
        The delete_review_by_id function deletes a review from the database.
        """
        try:
            if ReviewService.delete_review_by_id(review_id):
                return Response(content=f"Review with id {review_id} is deleted", status_code=200)
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err
