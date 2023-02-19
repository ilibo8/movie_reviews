"""Module for Reviews controller"""
from fastapi import HTTPException, Response
from sqlalchemy.exc import IntegrityError
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
            raise HTTPException(status_code=err.code, detail=err.message)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all_reviews():
        """
        The get_all_reviews function returns all reviews in the database.
        """
        try:
            return ReviewService.get_all_reviews()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_ratings_table():
        """
        The get_ratings_table function returns a table of all the ratings in the database.
        The function takes no arguments and returns a list of dictionaries, where each dictionary contains information
        about one rating.
        """
        try:
            return ReviewService.get_ratings_table()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_average_rating_for_movie(movie_title: str):
        """
        The get_average_rating_for_movie function accepts a movie title as an argument and returns the average
        rating for that movie. If no ratings are found, it raises a MovieNotFound exception.
        """
        try:
            return ReviewService.get_average_rating_for_movie(movie_title)
        except MovieNotFound as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

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
            raise HTTPException(status_code=err.code, detail=err.message)
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_reviews_by_user_name(user_name: str):
        """
        The get_reviews_by_user_name function is used to retrieve all reviews by a specific user.
        It takes in the user_name as an argument and returns a list of review objects.
        """
        try:
            return ReviewService.get_reviews_by_user_name(user_name)
        except UserNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

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
            raise HTTPException(status_code=err.code, detail=err.message)
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

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
            raise HTTPException(status_code=err.code, detail=err.message)
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

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
            raise HTTPException(status_code=err.code, detail=err.message)
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

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
            raise HTTPException(status_code=err.code, detail=err.message)
        except Unauthorized as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def delete_review_by_id(review_id: int):
        """
        The delete_review_by_id function deletes a review from the database.
        It takes in an integer representing the id of the review to be deleted, and returns a response object with either
        a status code of 200 or 500 depending on whether it was successful or not.
        """
        try:
            if ReviewService.delete_review_by_id(review_id):
                return Response(content=f"Review with id {review_id} is deleted", status_code=200)
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
