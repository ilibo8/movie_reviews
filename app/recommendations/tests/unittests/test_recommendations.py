"""Module for testing Recommendation repository methods."""
import pytest
from sqlalchemy.exc import IntegrityError

from app.groups.repository import GroupUserRepository, GroupRepository
from app.recommendations.exceptions import RecommendationNotFound
from app.recommendations.repository import RecommendationRepository
from app.tests import TestClass, TestingSessionLocal
from app.users.repository import UserRepository


class TestRecommendationsRepository(TestClass):
    """Class for testing Recommendation repository methods."""

    def create_foreign_keys(self):
        """Method for creating data necessary for testing."""
        with TestingSessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            user_repository = UserRepository(db)
            group_repository = GroupRepository(db)
            user_repository.create_user("user1", "pass", "user1@gmail.com")
            user_repository.create_user("user2", "pass", "user2@gmail.com")
            user_repository.create_user("user3", "pass", "user3@gmail.com")
            group_repository.add_group("g1", 1, "desc")
            group_repository.add_group("g2", 1, "desc")
            group_user_repository.add_group_user(1, 1)  # gu 1
            group_user_repository.add_group_user(1, 2)  # gu 2
            group_user_repository.add_group_user(1, 3)  # gu 3
            group_user_repository.add_group_user(2, 1)  # gu 4
            group_user_repository.add_group_user(2, 2)  # gu 5

    def test_add_post(self):
        """Test method add_post."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            recommendations_repo = RecommendationRepository(db)
            recommendation = recommendations_repo.add_post(1, "post")
            assert recommendation.post == "post"

    def test_add_post_error(self):
        """Test method add_post error."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            recommendations_repo = RecommendationRepository(db)
            with pytest.raises(IntegrityError):
                recommendations_repo.add_post(8, "post")

    def test_get_all_posts(self):
        """Test method get_all_posts"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            recommendations_repo = RecommendationRepository(db)
            recommendations_repo.add_post(1, "post")
            recommendations_repo.add_post(1, "post")
            recommendations_repo.add_post(2, "post")
            assert len(recommendations_repo.get_all_posts()) == 3

    def test_get_post_by_id(self):
        """Test method get post by id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            recommendations_repo = RecommendationRepository(db)
            recommendations_repo.add_post(1, "post1")
            recommendations_repo.add_post(1, "post")
            recommendations_repo.add_post(2, "post10")
            recommendations_repo.add_post(2, "post")
            post = recommendations_repo.get_post_by_id(3)
            assert post.id == 3
            assert post.group_user_id == 2
            assert post.post == "post10"

    def test_get_posts_by_id_error(self):
        """Test get_posts_by_id error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            recommendations_repo = RecommendationRepository(db)
            with pytest.raises(RecommendationNotFound):
                recommendations_repo.get_post_by_id(1)

    def test_get_all_posts_by_group_id(self):
        """Test method get_all_posts_by_group_id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            recommendations_repo = RecommendationRepository(db)
            recommendations_repo.add_post(1, "post1")
            recommendations_repo.add_post(2, "post2")
            recommendations_repo.add_post(3, "post3")
            recommendations_repo.add_post(4, "post4")
            recommendations_repo.add_post(5, "post5")
            posts = recommendations_repo.get_all_posts_by_group_id(2)
            assert len(posts) == 2
            assert posts[0].post == "post4"
            assert posts[1].group_user_id == 5

    def test_get_all_posts_by_user_id(self):
        """Test method get_all_posts_by_user_id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            recommendations_repo = RecommendationRepository(db)
            recommendations_repo.add_post(1, "post1")
            recommendations_repo.add_post(1, "post2")
            recommendations_repo.add_post(2, "post3")
            recommendations_repo.add_post(3, "post4")
            recommendations_repo.add_post(4, "post5")
            recommendations_repo.add_post(4, "post6")
            recommendations_repo.add_post(5, "post7")
            posts = recommendations_repo.get_all_posts_by_user_id(1)
            assert len(posts) == 4
            assert posts[3].post == "post6"

    def test_change_post_by_id(self):
        """Test change post by id."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            recommendations_repo = RecommendationRepository(db)
            recommendations_repo.add_post(1, "post")
            recommendations_repo.add_post(1, "post")
            recommendations_repo.change_post_by_id(2, "new post")
            post = recommendations_repo.get_post_by_id(2)
            assert post.post == "new post"

    def test_change_post_error(self):
        """Test change post raising error."""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            recommendations_repo = RecommendationRepository(db)
            with pytest.raises(RecommendationNotFound):
                recommendations_repo.change_post_by_id(1, "new post")

    def test_delete_post_by_id(self):
        """Test delete recommendation by id"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            recommendations_repo = RecommendationRepository(db)
            recommendations_repo.add_post(1, "post")
            assert recommendations_repo.delete_post_by_id(1) is True

    def test_delete_post_by_id_error(self):
        """Test delete_post_by_id error"""
        with TestingSessionLocal() as db:
            self.create_foreign_keys()
            recommendations_repo = RecommendationRepository(db)
            with pytest.raises(RecommendationNotFound):
                recommendations_repo.delete_post_by_id(1)
