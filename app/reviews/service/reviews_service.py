from app.db import SessionLocal
from app.reviews.repository import ReviewRepository


class ReviewService:

    @staticmethod
    def add_review(movie_id, user_id, rating_number, rating_description):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                return review_repository.add_review(movie_id, user_id, rating_number, rating_description)
        except Exception as e:
            raise e

    @staticmethod
    def get_all_reviews():
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                return review_repository.get_all_reviews()
        except Exception as e:
            raise e

    @staticmethod
    def get_reviews_by_movie_id(movie_id: int):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                return review_repository.get_reviews_by_movie_id(movie_id)
        except Exception as e:
            raise e

    @staticmethod
    def get_reviews_by_user_id(user_id: str):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                return review_repository.get_reviews_by_user_id(user_id)
        except Exception as e:
            raise e

    @staticmethod
    def change_movie_rating_number(movie_id: int, user_id: str, new_rating: int):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                return review_repository.change_movie_rating_number(movie_id, user_id, new_rating)
        except Exception as e:
            raise e

    @staticmethod
    def change_movie_rating_description(movie_id: int, user_id: str, new_description: str):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                return review_repository.change_movie_rating_description(movie_id, user_id, new_description)
        except Exception as e:
            raise e

    @staticmethod
    def delete_review_by_id(review_id: int):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                return review_repository.delete_review_by_id(review_id)
        except Exception as e:
            raise e
