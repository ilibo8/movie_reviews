"""Module for Recommendation servide."""
from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal
from app.groups.exceptions import GroupUserNotFound
from app.groups.repository import GroupRepository, GroupUserRepository
from app.recommendations.exceptions import RecommendationNotFound, Unauthorized
from app.recommendations.repository import RecommendationRepository


class RecommendationService:
    """Class for Recommendation service methods."""

    @staticmethod
    def add_post(group_name: str, user_id: int, post: str):
        """
        Method for adding new post.
        """
        try:
            with SessionLocal() as db:
                group_repository = GroupRepository(db)
                group_id = group_repository.get_group_id_by_name(group_name)
                recommendation_repo = RecommendationRepository(db)
                group_user_repo = GroupUserRepository(db)
                group_user_id = group_user_repo.get_id_by_user_and_group_id(group_id=group_id, user_id=user_id)
                if group_user_id is None:
                    raise Unauthorized(f"You are not member of group {group_name}")
                post = recommendation_repo.add_post(group_user_id, post)
                return {"post id" : post.id, "group name": group_name, "post" : post.post}
        except GroupUserNotFound as err:
            raise GroupUserNotFound(err.message) from err
        except IntegrityError as err:
            raise err

    @staticmethod
    def get_all_posts():
        """
        Method for getting all posts
        """
        try:
            with SessionLocal() as db:
                recommendation_repo = RecommendationRepository(db)
                return recommendation_repo.get_all_posts()
        except Exception as err:
            raise err

    @staticmethod
    def get_all_posts_by_group_name(group_name: str, user_id: int):
        """
        Method for getting all posts by group name with checking whether the user is member of group
        """
        try:
            with SessionLocal() as db:
                recommendation_repo = RecommendationRepository(db)
                group_user_repo = GroupUserRepository(db)
                if group_user_repo.check_if_user_is_part_of_group(group_name=group_name, user_id=user_id) is False:
                    raise Unauthorized(f"You are not part of group {group_name}")
                group_repo = GroupRepository(db)
                group_id = group_repo.get_group_id_by_name(group_name)
                posts = recommendation_repo.get_all_posts_by_group_id(group_id)
                all_posts = []
                for post in posts:
                    user_name = group_user_repo.get_user_name_by_group_user_id(post.group_user_id)
                    post_reformatted = {"user name" : user_name, "post": post.post}
                    print(post_reformatted)
                    all_posts.append(post_reformatted)
                return all_posts

        except GroupUserNotFound as err:
            raise GroupUserNotFound(err.message) from err
        except Exception as err:
            raise err

    @staticmethod
    def get_all_posts_by_user_id(user_id: int):
        """
        Get all posts added by user with provided id
        """
        try:
            with SessionLocal() as db:
                recommendation_repo = RecommendationRepository(db)
                group_user_repository = GroupUserRepository(db)
                group_repository = GroupRepository(db)
                all_posts = recommendation_repo.get_all_posts_by_user_id(user_id)
                if all_posts is None:
                    raise RecommendationNotFound("No data found")
                posts_reformatted = []
                for post in all_posts:
                    group_id = group_user_repository.get_group_id_by_group_user_id(post.group_user_id)
                    group_name = group_repository.get_group_name_by_id(group_id)
                    reformatted = {"group_name": group_name, "post_id": post.id, "post": post.post}
                    posts_reformatted.append(reformatted)
                return posts_reformatted
        except Exception as err:
            raise err

    @staticmethod
    def change_post_by_id(recommendation_id: int, user_id: int, new_post: str):
        """
        Change post of user by recommendation id
        """
        try:
            with SessionLocal() as db:
                recommendation_repo = RecommendationRepository(db)
                user_recommendation = recommendation_repo.get_all_posts_by_user_id(user_id)
                if recommendation_id not in user_recommendation:
                    raise Unauthorized("Access denied to other user's posts.")
                return recommendation_repo.change_post_by_id(recommendation_id, new_post)
        except RecommendationNotFound as err:
            raise RecommendationNotFound(err.message) from err
        except Exception as err:
            raise err

    @staticmethod
    def delete_post_id_by_user(recommendation_id: int, user_id: int):
        """
        The delete_post_id_by_user function deletes a post by recommendation id and user id.
        It takes in the following parameters: recommendation_id, user_id. It returns True if it is successful.
        """
        try:
            with SessionLocal() as db:
                recommendation_repo = RecommendationRepository(db)
                if recommendation_repo.delete_post_id_by_user(recommendation_id=recommendation_id, user_id=user_id):
                    return True
        except RecommendationNotFound as err:
            raise err
        except Unauthorized as err:
            raise err
        except Exception as err:
            raise err

    @staticmethod
    def delete_post_by_id(recommendation_id: int):
        """
        Delete post by id
        """
        try:
            with SessionLocal() as db:
                recommendation_repo = RecommendationRepository(db)
                if recommendation_repo.delete_post_by_id(recommendation_id):
                    return True
        except RecommendationNotFound as err:
            raise err
        except Exception as err:
            raise err
