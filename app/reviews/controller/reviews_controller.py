from fastapi import HTTPException, Response
from pymysql import IntegrityError

from app.reviews.exceptions import ReviewNotFound
from app.reviews.service import ReviewService


class ReviewController:

    @staticmethod
    def add_review(movie_id, user_id, rating_number, rating_description):
        try:
            return ReviewService.add_review(movie_id, user_id, rating_number, rating_description)
        except IntegrityError:
            raise HTTPException(status_code=400, detail=f"Error. Review for movie id {movie_id} already there.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_reviews():
        try:
            return ReviewService.get_all_reviews()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_reviews_by_movie_id(movie_id: int):
        try:
            return ReviewService.get_reviews_by_movie_id(movie_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_reviews_by_user_id(user_id: str):
        try:
            return ReviewService.get_reviews_by_user_id(user_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def change_movie_rating_number(movie_id: int, user_id: str, new_rating: int):
        try:
            return ReviewService.change_movie_rating_number(movie_id, user_id, new_rating)
        except ReviewNotFound as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def change_movie_rating_description(movie_id: int, user_id: str, new_description: str):
        try:
            return ReviewService.change_movie_rating_description(movie_id, user_id, new_description)
        except ReviewNotFound as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_review_by_id(review_id: int):
        try:
            if ReviewService.delete_review_by_id(review_id):
                return Response(content=f"Review with id {review_id} is deleted", status_code=200)
            return Response(content=f"Review with id {review_id} doesn't exist.", status_code=400)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
