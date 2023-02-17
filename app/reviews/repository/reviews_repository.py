from typing import Type

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.reviews.exceptions import ReviewNotFound, ReviewDuplicateEntry
from app.reviews.model import Review


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_review(self, movie_id: int, user_id: int, rating_number: int, review: str) -> Review:
        try:
            if self.db.query(Review).filter(and_(Review.movie_id == movie_id, Review.user_id == user_id)) is not None:
                raise ReviewDuplicateEntry(f"Review for movie id {movie_id} already exist.")
            review = Review(movie_id, user_id, rating_number, review)
            self.db.add(review)
            self.db.commit()
            self.db.refresh(review)
            return review
        except IntegrityError as e:
            raise e

    def get_all_reviews(self) -> list[Type[Review]]:
        reviews = self.db.query(Review).all()
        return reviews

    def get_reviews_by_movie_id(self, movie_id: int) -> list[Type[Review]]:
        reviews = self.db.query(Review).filter(Review.movie_id == movie_id).all()
        return reviews

    def get_reviews_by_user_id(self, user_id: int) -> list[Type[Review]]:
        reviews = self.db.query(Review).filter(Review.user_id == user_id).all()
        return reviews

    def change_movie_rating(self, movie_id: int, user_id: int, new_rating: int) -> Type[Review]:
        review = self.db.query(Review).filter(and_(Review.movie_id == movie_id, Review.user_id == user_id)).first()
        if review is None:
            raise ReviewNotFound(f"There is no review for movie_id {movie_id} for this user.")
        review.rating_number = new_rating
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def change_movie_review(self, movie_id: int, user_id: int, new_review: str) -> Type[Review]:
        review = self.db.query(Review).filter(and_(Review.movie_id == movie_id, Review.user_id == user_id)).first()
        if review is None:
            raise ReviewNotFound(f"There is no review for movie_id {movie_id} for this user.")
        review.review = new_review
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def delete_review_by_id(self, review_id: int) -> bool:
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if review is None:
            return False
        self.db.delete(review)
        self.db.commit()
        return True
