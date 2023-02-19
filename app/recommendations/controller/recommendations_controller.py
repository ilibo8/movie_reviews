"""Module for Recommendation controller layer"""
from fastapi import HTTPException, Response
from sqlalchemy.exc import IntegrityError
from app.groups.exceptions import GroupUserNotFound
from app.recommendations.exceptions import Unauthorized, RecommendationNotFound
from app.recommendations.service import RecommendationService


class RecommendationController:
    """Class for Recommendation controller layer methods"""

    @staticmethod
    def add_post(group_name: str, user_id: int, post: str):
        """
        The add_post function adds a post to the database.
        """
        try:
            return RecommendationService.add_post(group_name=group_name, user_id=user_id, post=post)
        except Unauthorized as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except GroupUserNotFound as err:
            raise HTTPException(status_code=err.code, detail=f"Error. You are not a member of group {group_name}.")
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all_posts():
        """
        The get_all_posts function returns all posts in the database.
        """
        try:
            return RecommendationService.get_all_posts()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all_posts_by_group_name(group_name: str, user_id: int):
        """
        The get_all_posts_by_group_name function is used to retrieve all posts from a group that the user has joined.
        It takes in two parameters, group_name and user_id. It then uses the get_all_posts function to retrieve all
        the posts from a specific group based on its name and returns them as an array of JSON objects.
        """
        try:
            return RecommendationService.get_all_posts_by_group_name(group_name, user_id)
        except Unauthorized as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except GroupUserNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all_posts_by_user_id(user_id: int):
        """
        The get_all_posts_by_user_id function is used to retrieve all the posts by a specific user.
        It takes in an integer representing the user id and returns a list of dictionaries containing
        the post information for each post made by that user.
        """
        try:
            return RecommendationService.get_all_posts_by_user_id(user_id)
        except RecommendationNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def change_post_by_id(recommendation_id: int, user_id: int, new_post: str):
        """
        The change_post_by_id function is used to change the post of a recommendation by id.
        It takes in an integer representing the id of a recommendation, an integer representing the user_id and
        a string containing the new post.
        """
        try:
            return RecommendationService.change_post_by_id(recommendation_id, user_id, new_post)
        except Unauthorized as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except RecommendationNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def delete_post_by_user(recommendation_id: int, user_id: int):
        """
        The delete_post_by_user function is used to delete a recommendation by the user.
        It takes in two parameters, recommendation_id and user_id. It then checks if the
        recommendation exists and if it does, it deletes that particular post from the database.
        """
        try:
            if RecommendationService.delete_post_id_by_user(recommendation_id, user_id):
                return Response(content=f"Recommendation with id {recommendation_id} is deleted", status_code=200)
        except Unauthorized as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except RecommendationNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def delete_post_by_id(recommendation_id: int):
        """
        The delete_post_by_id function deletes a recommendation from the database. It takes in an id as a parameter
        and returns True if it is able to delete the post, otherwise it raises an exception.
        """
        try:
            if RecommendationService.delete_post_by_id(recommendation_id):
                return Response(content=f"Recommendation with id {recommendation_id} is deleted", status_code=200)
        except RecommendationNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
