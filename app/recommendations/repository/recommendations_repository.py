"""Module for Recommendation repository"""
from typing import Type
from sqlalchemy.orm import Session
from app.groups.model import GroupUser
from app.recommendations.exceptions import RecommendationNotFound, Unauthorized
from app.recommendations.model import Recommendation


class RecommendationRepository:
    """Class for Recommendation repository"""

    def __init__(self, db: Session):
        self.db = db

    def add_post(self, group_user_id: int, post: str) -> Recommendation:
        """
        The add_post function adds a new post to the database.
        It takes in a group_user_id and post as arguments, and returns the newly created recommendation.
        """
        recommendation = Recommendation(group_user_id=group_user_id, post=post)
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation

    def get_all_posts(self) -> list[Type[Recommendation]]:
        """
        The get_all_posts function returns a list of all the Recommendation objects in the database.
        """
        return self.db.query(Recommendation).all()

    def get_post_by_id(self, recommendation_id: int) -> Type[Recommendation] | None:
        """
        The get_post_by_id function takes in a recommendation_id and returns the post with that id.
        If no such post exists, it raises a RecommendationNotFound error.
        """
        post = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if post is None:
            raise RecommendationNotFound(f"There is no post with id {recommendation_id}")
        return post

    def get_all_posts_by_group_id(self, group_id: int) -> list[Type[Recommendation]]:
        """
        The get_all_posts_by_group_id function takes in a group_id and returns all the recommendations for that group.
        It does this by joining Recommendation with GroupUser, which has a foreign key relationship to Recommendation.
        The function then filters the results by the given group_id.
        """
        recommendations = self.db.query(Recommendation). \
            join(GroupUser).filter(GroupUser.group_id == group_id).all()
        return recommendations

    def get_all_posts_by_user_id(self, user_id: int) -> list[Type[Recommendation]]:
        """
        The function takes in a user_id and returns all the posts that belong to that user.
        """
        recommendations = self.db.query(Recommendation). \
            join(GroupUser).filter(GroupUser.user_id == user_id).all()
        return recommendations

    def change_post_by_id(self, recommendation_id: int, new_post: str) -> Type[Recommendation]:
        """
        The function takes a recommendation id and new post as arguments.
        It finds the recommendation with that id, changes its post to the new_post argument,
        and returns it.
        """
        recommendation = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if recommendation is None:
            raise RecommendationNotFound(f"There is no post with id {recommendation_id}.")
        recommendation.post = new_post
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation

    def delete_post_id_by_user(self, recommendation_id: int, user_id: int) -> bool:
        """
        The delete_post_id_by_user function deletes a recommendation from the database.
        It first queries the database for a recommendation with the given id and then checks to see if that post
        was created by the user who is currently logged in. If it is not, then an error message will be raised.
        """
        recommendation = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if recommendation is None:
            raise RecommendationNotFound(f"There is no post with id {recommendation_id}.")
        group_user = self.db.query(GroupUser).join(Recommendation).filter(
            Recommendation.id == recommendation_id).first()
        if group_user.user_id != user_id:
            raise Unauthorized("Cannot delete other user's post.")
        self.db.delete(recommendation)
        self.db.commit()
        return True

    def delete_post_by_id(self, recommendation_id: int) -> bool:
        """
        The delete_post_by_id function deletes a recommendation from the database.
        It takes in an integer representing the id of the recommendation to be deleted, and returns True
        if it is successful.
        """
        recommendation = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if recommendation is None:
            raise RecommendationNotFound(f"There is no post with id {recommendation_id}.")
        self.db.delete(recommendation)
        self.db.commit()
        return True
