"""Module for Review repository testing"""

import pytest
from sqlalchemy.exc import IntegrityError

from app.movie.repository import MovieRepository
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
            with pytest.raises(IntegrityError):
                review_repository.add_review(1, 4, 5, "something")

    def test_add_review_error2(self):
        """Testing method add reviews for error2"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            review_repository = ReviewRepository(db)
            with pytest.raises(IntegrityError):
                review_repository.add_review(5, 2, 5, "something")

    def test_add_review_error3(self):
        """Testing method add reviews for error3"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            review_repository = ReviewRepository(db)
            with pytest.raises(ValueError):
                review_repository.add_review(1, 2, 0, "something")

    def test_add_review_error4(self):
        """Testing method add reviews for error4"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            review_repository = ReviewRepository(db)
            with pytest.raises(ValueError):
                review_repository.add_review(2, 2, 11, "something")

    def test_get_all_reviews(self):
        """Testing method get_all_reviews"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            review_repository = ReviewRepository(db)
            review_repository.add_review(1, 3, 5, "something")
            review_repository.add_review(2, 3, 5, "something")
            review_repository.add_review(1, 2, 5, "something")
            assert len(review_repository.get_all_reviews()) == 3

