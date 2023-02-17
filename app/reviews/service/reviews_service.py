from app.db import SessionLocal
from app.reviews.repository import ReviewRepository
from app.movie.repository import MovieRepository
from app.reviews.exceptions import ReviewNotFound
from app.users.repository import UserRepository


class ReviewService:

    @staticmethod
    def add_review(movie_name: str, user_id: int, rating_number: int, review: str):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_name)
                return review_repository.add_review(movie_id=movie_id, user_id=user_id, rating_number=rating_number,
                                                    review=review)
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
    def get_reviews_by_movie_title(movie_title: str):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                user_repository = UserRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_title)
                reviews = review_repository.get_reviews_by_movie_id(movie_id)
                if reviews is None:
                    raise ReviewNotFound(f"There is no review with movie id {movie_id}.")
                reviews_reformatted = []
                for review in reviews:
                    movie_title = movie_repository.get_title_by_id(review.movie_id)
                    user_name2 = user_repository.get_user_name_by_user_id(review.user_id)
                    reformatted = {"movie_title": movie_title, "user_name": user_name2,
                                   "rating_number": review.rating_number, "review": review.review}
                    reviews_reformatted.append(reformatted)
                return reviews_reformatted
        except Exception as err:
            raise err

    @staticmethod
    def get_reviews_by_user_name(user_name: str):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                user_repository = UserRepository(db)
                movie_repository = MovieRepository(db)
                user = user_repository.get_user_by_user_name(user_name)
                reviews = review_repository.get_reviews_by_user_id(user.id)
                if reviews is None:
                    raise ReviewNotFound(f"There is no review with user name {user_name}.")
                reviews_reformatted = []
                for review in reviews:
                    movie_title = movie_repository.get_title_by_id(review.movie_id)
                    user_name2 = user_repository.get_user_name_by_user_id(review.user_id)
                    reformatted = {"movie_title": movie_title, "user_name": user_name2,
                                   "rating_number": review.rating_number, "review": review.review}
                    reviews_reformatted.append(reformatted)
                return reviews_reformatted
        except Exception as err:
            raise err

    @staticmethod
    def change_movie_rating_number(movie_name: str, user_id: int, new_rating: int):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_name)
                return review_repository.change_movie_rating(movie_id, user_id, new_rating)
        except Exception as err:
            raise err

    @staticmethod
    def change_movie_review(movie_name: str, user_id: int, new_review: str):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_name)
                return review_repository.change_movie_review(movie_id, user_id, new_review)
        except Exception as err:
            raise err

    @staticmethod
    def delete_review_by_id(review_id: int):
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                return review_repository.delete_review_by_id(review_id)
        except Exception as err:
            raise err
