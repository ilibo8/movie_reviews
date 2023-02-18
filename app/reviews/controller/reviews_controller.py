from fastapi import HTTPException, Response
from sqlalchemy.exc import IntegrityError

from app.movie.exceptions import MovieNotFound
from app.reviews.exceptions import ReviewNotFound, ReviewDuplicateEntry, Unauthorized
from app.reviews.service import ReviewService
from app.users.exceptions import UserNotFound


class ReviewController:

    @staticmethod
    def add_review(movie_name: str, user_id: int, rating_number: int, review: str):
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
        try:
            return ReviewService.get_all_reviews()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_ratings_table():
        try:
            return ReviewService.get_ratings_table()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_average_rating_for_movie(movie_title: str):
        try:
            return ReviewService.get_average_rating_for_movie(movie_title)
        except MovieNotFound as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_reviews_by_movie_title(movie_title: str):
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
        try:
            if ReviewService.delete_review_by_id(review_id):
                return Response(content=f"Review with id {review_id} is deleted", status_code=200)
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
