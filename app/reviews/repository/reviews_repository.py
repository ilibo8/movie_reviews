from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.reviews.exceptions import ReviewNotFound
from app.reviews.model import Review


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_review(self, movie_id, user_id, rating_number, rating_description) -> Review:
        try:
            review = Review(movie_id, user_id, rating_number, rating_description)
            self.db.add(review)
            self.db.commit()
            self.db.refresh(review)
            return review
        except IntegrityError as e:
            raise e

    def get_all_reviews(self) -> list[Review]:
        reviews = self.db.query(Review).all()
        return reviews

    def get_reviews_by_movie_id(self, movie_id: int) -> list[Review]:
        reviews = self.db.query(Review).filter(Review.movie_id == movie_id).all()
        return reviews

    def get_reviews_by_user_id(self, user_id: str) -> list[Review]:
        reviews = self.db.query(Review).filter(Review.user_id == user_id).all()
        return reviews

    def change_movie_rating_number(self, movie_id: int, user_id: str, new_rating: int) -> Review:
        review = self.db.query(Review).filter(and_(Review.movie_id == movie_id, Review.user_id == user_id)).first()
        if review is None:
            raise ReviewNotFound(f"There is no review for movie_id {movie_id} for this user.")
        review.rating_number = new_rating
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def change_movie_rating_description(self, movie_id: int, user_id: str, new_description: str) -> Review:
        review = self.db.query(Review).filter(and_(Review.movie_id == movie_id, Review.user_id == user_id)).first()
        if review is None:
            raise ReviewNotFound(f"There is no review for movie_id {movie_id} for this user.")
        review.rating_description = new_description
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def delete_review_by_id(self, review_id: int) -> bool:
        try:
            review = self.db.query(Review).filter(Review.id == review_id).first()
            if review is None:
                return False
            self.db.delete(review)
            self.db.commit()
            return True
        except Exception as e:
            raise e
