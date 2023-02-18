from typing import Type

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.reviews.exceptions import ReviewNotFound, ReviewDuplicateEntry, Unauthorized
from app.reviews.model import Review


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_review(self, movie_id: int, user_id: int, rating_number: int, review: str) -> Review:
        try:
            review = Review(movie_id, user_id, rating_number, review)
            self.db.add(review)
            self.db.commit()
            self.db.refresh(review)
            return review
        except IntegrityError:
            raise ReviewDuplicateEntry("Rating and review already exist for this movie.")

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
            raise ReviewNotFound("There is no review for this user.")
        review.review = new_review
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def delete_review_id_by_user(self, review_id: int, user_id: int):
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if review is None:
            raise ReviewNotFound(f"There is no review with id {review_id}.")
        if review.user_id != user_id:
            raise Unauthorized("Can't delete other user's review.")
        self.db.delete(review)
        self.db.commit()
        return True

    def delete_review_by_id(self, review_id: int):
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if review is None:
            raise ReviewNotFound(f"There is no review with id {review_id}.")
        self.db.delete(review)
        self.db.commit()
        return True
