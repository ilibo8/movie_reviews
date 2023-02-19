"""Module for Review repository testing"""
import pytest
from app.movie.repository import MovieRepository
from app.reviews.exceptions import ReviewDuplicateEntry, ReviewNotFound, Unauthorized
from app.reviews.repository import ReviewRepository
from app.tests import TestClass, TestingSessionLocal
from app.users.repository import UserRepository


class TestReviewRepository(TestClass):
    """Class for testing methods for ReviewRepository"""

    def create_foreign_keys(self):
        with TestingSessionLocal() as dbs:
            user_repository = UserRepository(dbs)
            movie_repository = MovieRepository(dbs)
            user_repository.create_user("user1", "pass", "user1@gmail.com")
            user_repository.create_user("user2", "pass", "user2@gmail.com")
            user_repository.create_user("user3", "pass", "user3@gmail.com")
            movie_repository.add_movie("red", "dir1", 2000, "USA")
            movie_repository.add_movie("blue", "dir2", 2005, "France")
            movie_repository.add_movie("orange", "dir3", 2010, "Serbia")

    def test_get_average_rating_by_movie_id(self):
        """Testing method get_average_rating_by_movie_id"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review_repository.add_review(1, 3, 5, "something")
            review_repository.add_review(2, 3, 6, "something")
            review_repository.add_review(1, 2, 7, "something")
            review_repository.add_review(2, 2, 7, "something")
            review_repository.add_review(2, 1, 8, "something")
            assert review_repository.get_average_rating_and_count_by_movie_id(1) == (6.00, 2)
            assert review_repository.get_average_rating_and_count_by_movie_id(2) == (7.00, 3)

    def test_add_review(self):
        """Test method add_review."""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review = review_repository.add_review(1, 3, 5, "something")
            assert review.movie_id == 1
            assert review.user_id == 3
            assert review.rating_number == 5
            assert review.review == "something"

    def test_add_review_error(self):
        """Testing method add reviews for error"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review_repository.add_review(1, 3, 6, "something")
            with pytest.raises(ReviewDuplicateEntry):
                review_repository.add_review(1, 3, 5, "something")

    def test_get_all_reviews(self):
        """Testing method get_all_reviews"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review_repository.add_review(1, 3, 5, "something")
            review_repository.add_review(2, 3, 5, "something")
            review = review_repository.add_review(1, 2, 5, "something")
            assert len(review_repository.get_all_reviews()) == 3
            assert review.rating_number == 5

    def test_get_reviews_by_movie_id(self):
        """Testing method get_reviews_by_movie_id"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review_repository.add_review(1, 3, 5, "something")
            review_repository.add_review(2, 3, 6, "something")
            review_repository.add_review(1, 2, 7, "something")
            review_repository.add_review(3, 2, 8, "something")
            review_repository.add_review(2, 2, 9, "something")
            assert len(review_repository.get_reviews_by_movie_id(1)) == 2

    def test_get_reviews_by_user_id(self):
        """Testing method get_reviews_by_user_id"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review_repository.add_review(1, 3, 5, "something")
            review_repository.add_review(2, 3, 6, "something")
            review_repository.add_review(1, 2, 7, "something")
            review_repository.add_review(3, 2, 8, "something")
            review_repository.add_review(2, 2, 9, "something")
            assert len(review_repository.get_reviews_by_user_id(3)) == 2
            assert review_repository.get_reviews_by_user_id(3)[1].rating_number == 6

    def test_get_ratings_table(self):
        """Testing method get_ratings_table"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review_repository.add_review(1, 3, 5, "something")
            review_repository.add_review(2, 3, 6, "something")
            review_repository.add_review(1, 2, 7, "something")
            review_repository.add_review(2, 2, 7, "something")
            review_repository.add_review(2, 1, 8, "something")
            ratings_list = review_repository.get_ratings_table()
            assert len(ratings_list) == 2

    def test_change_movie_rating(self):
        """Testing method change movie rating"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review_repository.add_review(1, 3, 5, "something")
            new_rating = review_repository.change_movie_rating(1, 3, 8)
            assert new_rating.id == 1
            assert new_rating.rating_number == 8

    def test_change_movie_rating_error2(self):
        """Testing method change movie rating error"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            with pytest.raises(ReviewNotFound):
                review_repository.change_movie_rating(10, 2, 5)

    def test_change_movie_review(self):
        """Testing method change movie review"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review_repository.add_review(1, 3, 5, "something")
            new_review = review_repository.change_movie_review(1, 3, "new review")
            assert new_review.id == 1
            assert new_review.review == "new review"

    def test_change_movie_review_error2(self):
        """Testing method change movie review error"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            with pytest.raises(ReviewNotFound):
                review_repository.change_movie_review(10, 2, "new review")

    def test_delete_review_id_by_user(self):
        """Testing method delete review id by user"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review_repository.add_review(1, 3, 5, "something")
            assert review_repository.delete_review_id_by_user(1, 3) is True

    def test_delete_review_id_by_user_error(self):
        """Testing method delete review id by user error"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            with pytest.raises(ReviewNotFound):
                review_repository.delete_review_id_by_user(10, 2)

    def test_delete_review_id_by_user_error2(self):
        """Testing method delete review id by user error"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review_repository.add_review(1, 3, 5, "something")
            with pytest.raises(Unauthorized):
                review_repository.delete_review_id_by_user(1, 4)

    def test_delete_review_id(self):
        """Testing method delete review id"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            review_repository.add_review(1, 3, 5, "something")
            assert review_repository.delete_review_by_id(1) is True

    def test_delete_review_id_error(self):
        """Testing method delete review id error"""
        with TestingSessionLocal() as dbs:
            self.create_foreign_keys()
            review_repository = ReviewRepository(dbs)
            with pytest.raises(ReviewNotFound):
                review_repository.delete_review_by_id(10)
