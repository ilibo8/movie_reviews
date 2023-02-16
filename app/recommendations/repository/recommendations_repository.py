"""Module for Recommendation repository"""
from typing import Type
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.groups.model import GroupUser
from app.recommendations.exceptions import RecommendationNotFound
from app.recommendations.model import Recommendation


class RecommendationRepository:
    """Class for Recommendation repository"""

    def __init__(self, db: Session):
        self.db = db

    def add_post(self, group_user_id: int, post: str) -> Recommendation:
        """Method for creating new recommendation"""
        try:
            recommendation = Recommendation(group_user_id=group_user_id, post=post)
            self.db.add(recommendation)
            self.db.commit()
            self.db.refresh(recommendation)
            return recommendation
        except IntegrityError as err:
            raise err

    def get_all_posts(self) -> list[Type[Recommendation]]:
        """Method for getting all posts."""
        return self.db.query(Recommendation).all()

    def get_post_by_id(self, recommendation_id: int) -> Type[Recommendation] | None:
        """Method for getting posts by id."""
        post = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if post is None:
            raise RecommendationNotFound(f"No post with id {recommendation_id}")
        return post

    def get_all_posts_by_group_id(self, group_id: int) -> list[Type[Recommendation]]:
        """Method for getting all posts for one group."""
        # group_users = self.db.query(GroupUser).filter(GroupUser.group_id == group_id).all()
        # if group_users is None:
        #     raise GroupUserNotFound(f"Group user for group id {group_id} not found")
        # group_users_ids = [x.id for x in group_users]
        # recommendations = []
        # for id in group_users_ids:
        #     recommendation = self.db.query(Recommendation).filter(Recommendation.group_user_id == id).all()
        #     for item in recommendation:
        #         recommendations.append(item)
        recommendations = self.db.query(Recommendation). \
            join(GroupUser).filter(GroupUser.group_id == group_id).all()
        return recommendations

    def get_all_posts_by_user_id(self, user_id: int) -> list[Type[Recommendation]]:
        """Method for getting all posts for one group."""
        recommendations = self.db.query(Recommendation). \
            join(GroupUser).filter(GroupUser.user_id == user_id).all()
        return recommendations

    def change_post_by_id(self, recommendation_id: int, new_post: str) -> Type[Recommendation]:
        """Method for changing post of user."""
        recommendation = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if recommendation is None:
            raise RecommendationNotFound(f"There is no recommendation with id {recommendation_id}.")
        recommendation.post = new_post
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation

    def delete_post_by_id(self, recommendation_id: int) -> bool:
        """Method for deleting post"""
        recommendation = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if recommendation is None:
            raise RecommendationNotFound(f"There is no recommendation with id {recommendation_id}.")
        self.db.delete(recommendation)
        self.db.commit()
        return True
