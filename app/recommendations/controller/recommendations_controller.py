from fastapi import HTTPException, Response
from sqlalchemy.exc import IntegrityError

from app.groups.exceptions import GroupUserNotFound
from app.recommendations.exceptions import Unauthorized, RecommendationNotFound
from app.recommendations.service import RecommendationService


class RecommendationController:

    @staticmethod
    def add_post(group_name: str, user_id: int, post: str):
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
        try:
            return RecommendationService.get_all_posts()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_posts_by_group_name(group_name: str, user_id: int):
        try:
            return RecommendationService.get_all_posts_by_group_name(group_name, user_id)
        except Unauthorized as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except GroupUserNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_posts_by_user_id(user_id: int):
        try:
            return RecommendationService.get_all_posts_by_user_id(user_id)
        except RecommendationNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def change_post_by_id(recommendation_id: int, user_id: int, new_post: str):
        try:
            return RecommendationService.change_post_by_id(recommendation_id, user_id, new_post)
        except Unauthorized as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except RecommendationNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def delete_post_by_id(recommendation_id: int, user_id: int):
        try:
            if RecommendationService.delete_post_by_id(recommendation_id, user_id):
                return Response(content=f"Recommendation with id {recommendation_id} is deleted", status_code=200)
        except Unauthorized as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except RecommendationNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
