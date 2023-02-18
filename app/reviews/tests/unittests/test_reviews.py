"""Module for Review repository testing"""

import pytest


from app.movie.repository import MovieRepository
from app.reviews.exceptions import ReviewDuplicateEntry
from app.reviews.repository import ReviewRepository
from app.tests import TestClass, TestingSessionLocal
from app.users.repository import UserRepository


class TestReviewRepository(TestClass):
    """Class for testing methods for ReviewRepository"""

    def create_foreign_keys(self):
        with TestingSessionLocal() as db:
            user_repository = UserRepository(db)
            movie_repository = MovieRepository(db)
            user_repository.create_user("user1", "pass", "user1@gmail.com")
            user_repository.create_user("user2", "pass", "user2@gmail.com")
            user_repository.create_user("user3", "pass", "user3@gmail.com")
            movie_repository.add_movie("red", "dir1", 2000, "USA")
            movie_repository.add_movie("blue", "dir2", 2005, "France")
            movie_repository.add_movie("orange", "dir3", 2010, "Serbia")

    def test_get_average_rating_by_movie_id(self):
        """Testing method get_average_rating_by_movie_id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            review_repository = ReviewRepository(db)
            review_repository.add_review(1, 3, 5, "something")
            review_repository.add_review(2, 3, 6, "something")
            review_repository.add_review(1, 2, 7, "something")
            review_repository.add_review(2, 2, 7, "something")
            review_repository.add_review(2, 1, 8, "something")
            assert review_repository.get_average_rating_by_movie_id(1)[0] == 6.00
            assert review_repository.get_average_rating_by_movie_id(2)[0] == 7.00
            assert review_repository.get_average_rating_by_movie_id(1)[1] == 2
            assert review_repository.get_average_rating_by_movie_id(2)[1] == 3



    def test_add_review(self):
        """Test method add_review."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            review_repository = ReviewRepository(db)
            review = review_repository.add_review(1, 3, 5, "something")
            assert review.movie_id == 1
            assert review.user_id == 3
            assert review.rating_number == 5
            assert review.review == "something"

    def test_add_review_error(self):
        """Testing method add reviews for error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            review_repository = ReviewRepository(db)
            review_repository.add_review(1, 3, 6, "something")
            with pytest.raises(ReviewDuplicateEntry):
                review_repository.add_review(1, 3, 5, "something")

    def test_get_all_reviews(self):
        """Testing method get_all_reviews"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            review_repository = ReviewRepository(db)
            review_repository.add_review(1, 3, 5, "something")
            review_repository.add_review(2, 3, 5, "something")
            review = review_repository.add_review(1, 2, 5, "something")
            assert len(review_repository.get_all_reviews()) == 3
            assert review.rating_number == 5

    def test_get_reviews_by_movie_id(self):
        """Testing method get_reviews_by_movie_id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            review_repository = ReviewRepository(db)
            review_repository.add_review(1, 3, 5, "something")
            review_repository.add_review(2, 3, 6, "something")
            review_repository.add_review(1, 2, 7, "something")
            review_repository.add_review(3, 2, 8, "something")
            review_repository.add_review(2, 2, 9, "something")
            assert len(review_repository.get_reviews_by_movie_id(1)) == 2

    def test_get_reviews_by_user_id(self):
        """Testing method get_reviews_by_user_id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            review_repository = ReviewRepository(db)
            review_repository.add_review(1, 3, 5, "something")
            review_repository.add_review(2, 3, 6, "something")
            review_repository.add_review(1, 2, 7, "something")
            review_repository.add_review(3, 2, 8, "something")
            review_repository.add_review(2, 2, 9, "something")
            assert len(review_repository.get_reviews_by_user_id(3)) == 2
            assert review_repository.get_reviews_by_user_id(3)[1].rating_number == 6
