"""Module for Review repository"""
from typing import Type
from sqlalchemy import and_, func, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.reviews.exceptions import ReviewNotFound, ReviewDuplicateEntry, Unauthorized
from app.reviews.model import Review


class ReviewRepository:
    """Class for Review repository methods"""

    def __init__(self, dbs: Session):
        self.dbs = dbs

    def add_review(self, movie_id: int, user_id: int, rating_number: int, review: str) -> Review:
        """
        The add_review function adds a review to the database.
        It takes in movie_id, user_id, rating_number and review as parameters.
        If the rating and review already exist for this movie then it raises an error.
        """
        try:
            if self.dbs.query(Review).filter(
                    and_(Review.movie_id == movie_id, Review.user_id == user_id)).first() is not None:
                raise ReviewDuplicateEntry("Rating and review already exist for this movie.")
            review = Review(movie_id, user_id, rating_number, review)
            self.dbs.add(review)
            self.dbs.commit()
            self.dbs.refresh(review)
            return review
        except IntegrityError as err:
            raise IntegrityError from err

    def get_all_reviews(self) -> list[Type[Review]]:
        """
        The get_all_reviews function returns a list of all reviews in the database.
        """
        reviews = self.dbs.query(Review).all()
        return reviews

    def get_reviews_by_movie_id(self, movie_id: int) -> list[Type[Review]]:
        """
        The get_reviews_by_movie_id function takes a movie_id as an argument and returns all the reviews for that movie.
        It queries the database to find all reviews with a matching movie_id, then returns them.
        """
        reviews = self.dbs.query(Review).filter(Review.movie_id == movie_id).all()
        return reviews

    def get_reviews_by_user_id(self, user_id: int) -> list[Type[Review]]:
        """
        The get_reviews_by_user_id function takes a user_id as an argument and returns all the reviews that have been
        written by that user. It does this by querying the database for all reviews where the review's user_id matches
        the passed in parameter. The function then returns a list of Review objects.
        """
        reviews = self.dbs.query(Review).filter(Review.user_id == user_id).all()
        return reviews

    def get_average_rating_and_count_by_movie_id(self, movie_id: int) -> (float, int):
        """
        The get_average_rating_and_count_by_movie_id function takes in a movie_id and returns the average rating
        and count of ratings for that movie. It does this by querying the database for all reviews with a given
        movie_id, then calculating the average rating and count of ratings.
        """
        avg = self.dbs.query(func.round(func.avg(Review.rating_number), 2)).filter(Review.movie_id == movie_id).scalar()
        count = self.dbs.query(func.count(Review.rating_number)).filter(Review.movie_id == movie_id).scalar()
        return avg, count

    def get_ratings_table(self) -> list:
        """
        The get_ratings_table function returns a list of dictionaries with the movie title and average rating.
        The function uses a sql statement to get the movies and their ratings from the reviews table. The function then
        sorts this list by highest rating first.
        """
        sql = """select movies.title, avg(reviews.rating_number) as avg_number from movies join reviews on movies.id =
        reviews.movie_id group by movies.id; """
        result = self.dbs.execute(text(sql))
        result_table = []
        for row in result:
            result_table.append({"title": row[0], "rating": round(float(row[1]), 2)})
        sorted_list = sorted(result_table, key=lambda x: x['rating'], reverse=True)
        return sorted_list

    def change_movie_rating(self, movie_id: int, user_id: int, new_rating: int) -> Type[Review]:
        """
        The change_movie_rating function takes in a movie_id, user_id and new rating.
        It then checks if the review exists for that movie and user. If it does not exist,
        it raises a ReviewNotFound exception. If it does exist, it changes the rating to
        the new rating.
        """
        review = self.dbs.query(Review).filter(and_(Review.movie_id == movie_id, Review.user_id == user_id)).first()
        if review is None:
            raise ReviewNotFound(f"There is no review for movie_id {movie_id} for this user.")
        review.rating_number = new_rating
        self.dbs.add(review)
        self.dbs.commit()
        self.dbs.refresh(review)
        return review

    def change_movie_review(self, movie_id: int, user_id: int, new_review: str) -> Type[Review]:
        """
        The change_movie_review function takes in a movie_id, user_id and new review. It then queries the database
        for a review matching both the movie id and user id. If there is no such review, it raises an exception.
        Otherwise, it changes the old review to be equal to new_review.
        """
        review = self.dbs.query(Review).filter(and_(Review.movie_id == movie_id, Review.user_id == user_id)).first()
        if review is None:
            raise ReviewNotFound("There is no review for this user.")
        review.review = new_review
        self.dbs.add(review)
        self.dbs.commit()
        self.dbs.refresh(review)
        return review

    def delete_review_id_by_user(self, review_id: int, user_id: int):
        """
        The delete_review_id_by_user function deletes a review from the database.
        It takes two arguments, review_id and user_id. It first queries the database for a review with that id,
        if it finds one it checks to see if that reviews user id matches the users id passed in as an argument.
        If they match then it will delete that record from the database and return True otherwise it raises an error.
        """
        review = self.dbs.query(Review).filter(Review.id == review_id).first()
        if review is None:
            raise ReviewNotFound(f"There is no review with id {review_id}.")
        if review.user_id != user_id:
            raise Unauthorized("Can't delete other user's review.")
        self.dbs.delete(review)
        self.dbs.commit()
        return True

    def delete_review_by_id(self, review_id: int):
        """
        The delete_review_by_id function deletes a review from the database.
        It takes in an integer representing the id of the review to be deleted, and returns True if successful.
        """
        review = self.dbs.query(Review).filter(Review.id == review_id).first()
        if review is None:
            raise ReviewNotFound(f"There is no review with id {review_id}.")
        self.dbs.delete(review)
        self.dbs.commit()
        return True
