"""Module for Review repository"""
from typing import Type
from sqlalchemy import and_, func, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.movie.model import MovieGenre
from app.reviews.exceptions import ReviewNotFound, ReviewDuplicateEntry
from app.reviews.model import Review
from app.users.exceptions import UserNotFound
from app.users.model import User


class ReviewRepository:
    """Class for Review repository methods"""

    def __init__(self, db: Session):
        self.db = db

    def add_review(self, movie_id: int, user_id: int, rating_number: int, review: str) -> Review:
        """
        The add_review function adds a review to the database.
        It takes in movie_id, user_id, rating_number and review as parameters.
        If the rating and review already exist for this movie then it raises an error.
        """
        try:
            if self.db.query(Review).filter(
                    and_(Review.movie_id == movie_id, Review.user_id == user_id)).first() is not None:
                raise ReviewDuplicateEntry("Review already exist for this movie.")
            review = Review(movie_id, user_id, rating_number, review)
            self.db.add(review)
            self.db.commit()
            self.db.refresh(review)
            return review
        except IntegrityError as err:
            raise IntegrityError from err

    def get_all_reviews(self) -> list[Type[Review]]:
        """
        The get_all_reviews function returns a list of all reviews in the database.
        """
        reviews = self.db.query(Review).all()
        return reviews

    def get_reviews_by_movie_id(self, movie_id: int) -> list[Type[Review]]:
        """
        The get_reviews_by_movie_id function takes a movie_id as an argument and returns all the reviews for that movie.
        It queries the database to find all reviews with a matching movie_id, then returns them.
        """
        reviews = self.db.query(Review).filter(Review.movie_id == movie_id).all()
        return reviews

    def get_reviews_by_user_id(self, user_id: int) -> list[Type[Review]]:
        """
        The get_reviews_by_user_id function takes a user_id as an argument and returns all the reviews that have been
        written by that user. It does this by querying the database for all reviews where the review's user_id matches
        the passed in parameter. The function then returns a list of Review objects.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise UserNotFound(f"There is no user with id {user_id}")
        reviews = self.db.query(Review).filter(Review.user_id == user_id).all()
        return reviews

    def get_reviews_by_user_id_and_movie_id(self, movie_id: int, user_id: int) -> Type[Review] | None:
        """
        The function takes a user_id and movie_id as arguments and returns review.
        """
        return self.db.query(Review).filter(and_(Review.user_id == user_id, Review.movie_id == movie_id)).first()

    def get_review_by_id(self, review_id: int) -> Type[Review] | None:
        """
        The function accepts a review_id as an argument and returns the Review object associated with that id.
        """
        return self.db.query(Review).filter(Review.id == review_id).first()

    def get_top_five_users_with_most_reviews(self):
        """
        Returns top 5 users by number of their reviews. Returns list[(user_id, no. of reviews))].
        """
        subquery = self.db.query(Review.user_id, func.count(Review.user_id).label("count")).group_by(Review.user_id) \
            .subquery()
        users = self.db.query(subquery).order_by(desc("count")).limit(5).all()
        return users

    def get_top_n_movies_by_avg_rating(self, number_of_movies: int):
        """
        Returns top n movies by their average rating. Returns list[(movie_id, avg_rating, number_of_ratings)]
        """
        subquery = self.db.query(Review.movie_id, func.round(func.avg(Review.rating_number), 2).label("avg"),
                                 func.count(Review.rating_number).label("count")).group_by(Review.movie_id).subquery()
        movies = self.db.query(subquery).order_by(desc("avg")).limit(number_of_movies).all()
        return movies

    def get_five_best_rated_movies_by_genre(self, genre: str):
        """
        Returns top n movies of certain genre by their average rating. Returns list[(movie_id, avg_rating, user_rated)]
        """
        movie_ids = self.db.query(MovieGenre.movie_id).filter(MovieGenre.genre_name == genre).distinct().all()
        movie_ids = [x[0] for x in movie_ids]
        subquery = self.db.query(Review.movie_id, func.round(func.avg(Review.rating_number), 2).label("avg"),
                                 func.count(Review.rating_number).label("count")).group_by(Review.movie_id).filter \
            (Review.movie_id.in_(movie_ids)).subquery()
        movies = self.db.query(subquery).order_by(desc("avg")).limit(5).all()
        return movies

    def get_average_rating_and_count_by_movie_id(self, movie_id: int):
        """
        The get_average_rating_and_count_by_movie_id function takes in a movie_id and returns the average rating
        and count of ratings for that movie. It does this by querying the database for all reviews with a given
        movie_id, then calculating the average rating and count of ratings.
        """
        avg = self.db.query(func.round(func.avg(Review.rating_number), 2)).filter(Review.movie_id == movie_id).scalar()
        count = self.db.query(func.count(Review.rating_number)).filter(Review.movie_id == movie_id).scalar()
        if count == 0:
            return 0, 0
        return avg, count

    def change_movie_rating(self, movie_id: int, user_id: int, new_rating: int) -> Type[Review]:
        """
        The change_movie_rating function takes in a movie_id, user_id and new rating.
        It then checks if the review exists for that movie and user. If it does not exist,
        it raises a ReviewNotFound exception. If it does exist, it changes the rating to
        the new rating.
        """
        review = self.db.query(Review).filter(and_(Review.movie_id == movie_id, Review.user_id == user_id)).first()
        if review is None:
            raise ReviewNotFound("There is no review for this movie.")
        review.rating_number = new_rating
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def change_movie_review(self, movie_id: int, user_id: int, new_review: str) -> Type[Review]:
        """
        The change_movie_review function takes in a movie_id, user_id and new review. It then queries the database
        for a review matching both the movie id and user id. If there is no such review, it raises an exception.
        Otherwise, it changes the old review to be equal to new_review.
        """
        review = self.db.query(Review).filter(and_(Review.movie_id == movie_id, Review.user_id == user_id)).first()
        if review is None:
            raise ReviewNotFound("There is no review for this movie.")
        review.review = new_review
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def delete_review_by_id(self, review_id: int):
        """
        The delete_review_by_id function deletes a review from the database.
        It takes in an integer representing the id of the review to be deleted, and returns True if successful.
        """
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if review is None:
            raise ReviewNotFound(f"There is no review with id {review_id}.")
        self.db.delete(review)
        self.db.commit()
        return True
