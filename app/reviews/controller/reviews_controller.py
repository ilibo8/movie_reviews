from fastapi import HTTPException, Response
from pymysql import IntegrityError

from app.movie.exceptions import MovieNotFound
from app.reviews.exceptions import ReviewNotFound, ReviewDuplicateEntry
from app.reviews.service import ReviewService


class ReviewController:

    @staticmethod
    def add_review(movie_id: int, user_id: int, rating_number: int, review: str):
        try:
            return ReviewService.add_review(movie_id, user_id, rating_number, review)
        except ReviewDuplicateEntry as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all_reviews():
        try:
            return ReviewService.get_all_reviews()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_reviews_by_movie_title(movie_title: str):
        try:
            return ReviewService.get_reviews_by_movie_title(movie_title)
        except MovieNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except ReviewNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_reviews_by_user_name(user_name: str):
        try:
            return ReviewService.get_reviews_by_user_name(user_name)
        except ReviewNotFound as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def change_movie_rating_number(movie_id: int, user_id: int, new_rating: int):
        try:
            return ReviewService.change_movie_rating_number(movie_id, user_id, new_rating)
        except ReviewNotFound as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def change_movie_review(movie_id: int, user_id: int, new_review: str):
        try:
            return ReviewService.change_movie_review(movie_id, user_id, new_review)
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
