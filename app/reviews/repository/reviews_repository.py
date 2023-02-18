from typing import Type

from sqlalchemy import and_, func, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.reviews.exceptions import ReviewNotFound, ReviewDuplicateEntry, Unauthorized
from app.reviews.model import Review


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_review(self, movie_id: int, user_id: int, rating_number: int, review: str) -> Review:
        try:
            if self.db.query(Review).filter(
                    and_(Review.movie_id == movie_id, Review.user_id == user_id)).first() is not None:
                raise ReviewDuplicateEntry("Rating and review already exist for this movie.")
            review = Review(movie_id, user_id, rating_number, review)
            self.db.add(review)
            self.db.commit()
            self.db.refresh(review)
            return review
        except IntegrityError:
            raise IntegrityError

    def get_all_reviews(self) -> list[Type[Review]]:
        reviews = self.db.query(Review).all()
        return reviews

    def get_reviews_by_movie_id(self, movie_id: int) -> list[Type[Review]]:
        reviews = self.db.query(Review).filter(Review.movie_id == movie_id).all()
        return reviews

    def get_reviews_by_user_id(self, user_id: int) -> list[Type[Review]]:
        reviews = self.db.query(Review).filter(Review.user_id == user_id).all()
        return reviews

    def get_average_rating_and_count_by_movie_id(self, movie_id: int) -> (float, int):
        avg = self.db.query(func.round(func.avg(Review.rating_number), 2)).filter(Review.movie_id == movie_id).scalar()
        count = self.db.query(func.count(Review.rating_number)).filter(Review.movie_id == movie_id).scalar()
        return avg, count

    def get_ratings_table(self):
        """Getting table with all movies and their average ratings using sql statement."""
        sql = """select movies.title, avg(reviews.rating_number) as avg_number from movies join reviews on movies.id =
        reviews.movie_id group by movies.id; """
        result = self.db.execute(text(sql))
        result_table = []
        for row in result:
            result_table.append({"title": row[0], "rating": round(float(row[1]), 2)})
        sorted_list = sorted(result_table, key=lambda x: x['rating'], reverse=True)
        return sorted_list

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
