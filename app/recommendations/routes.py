"""Module for routes for group recommendations"""
from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.recommendations.schema import RecommendationSchema, RecommendationSchemaOut
from app.users.controller import JWTBearer, extract_user_id_from_token
from app.recommendations.controller import RecommendationController

recommendations_router = APIRouter(prefix="/api/recommendations", tags=["Group Recommendations"])
recommendations_superuser_router = APIRouter(prefix="/api/superuser/recommendations",
                                             tags=["superuser - Groups & Recommendations"])


@recommendations_router.get("/get-all-your-posts", response_model=list[RecommendationSchemaOut],
                            dependencies=[Depends(JWTBearer("classic_user"))])
def get_all_your_posts(request: Request):
    """
    The function returns a list of all post made by user requesting it.
    """
    user_id = extract_user_id_from_token(request)
    return RecommendationController.get_all_posts_by_user_id(user_id)


@recommendations_router.get("/get-all-posts-from-your-group",
                            dependencies=[Depends(JWTBearer("classic_user"))])
def get_all_posts_from_your_group(group_name: str, request: Request):
    """
    The function returns a list of all post made in group of request.
    """
    user_id = extract_user_id_from_token(request)
    return RecommendationController.get_all_posts_by_group_name(group_name=group_name, user_id=user_id)


@recommendations_router.post("/add-post-to-your-group", dependencies=[Depends(JWTBearer("classic_user"))])
def add_post_to_your_group(group_name: str, post: str, request: Request):
    """
    The function adds a post made by user to group of request.
    """
    user_id = extract_user_id_from_token(request)
    return RecommendationController.add_post(group_name=group_name, user_id=user_id, post=post)


@recommendations_router.delete("/delete-post-by-its-id/{post_id}", dependencies=[Depends(JWTBearer("classic_user"))])
def delete_post_by_its_id(post_id: int, request: Request):
    """
    The function deletes the post by its id. First it checks that this post belongs to user trying to delete it.
    """
    user_id = extract_user_id_from_token(request)
    return RecommendationController.delete_post_by_user(recommendation_id=post_id, user_id=user_id)


@recommendations_superuser_router.get("/get-all-posts", response_model=list[RecommendationSchema],
                                      dependencies=[Depends(JWTBearer("super_user"))])
def get_all_posts():
    """
    The function returns list of all posts with user and post ids.
    """
    return RecommendationController.get_all_posts()


@recommendations_superuser_router.get("/get-all-posts-by-user-id/{user_id}",
                                      response_model=list[RecommendationSchema],
                                      dependencies=[Depends(JWTBearer("super_user"))])
def get_all_posts_by_user(user_id: int):
    """
    The function returns list of all posts with user and post ids.
    """
    return RecommendationController.get_all_posts_by_user_id(user_id)


@recommendations_superuser_router.delete("/delete-post-by-its-id/{post_id}",
                                         dependencies=[Depends(JWTBearer("super_user"))])
def delete_post_by_id(post_id: int):
    """
    The function deletes the post by its id.
    """
    return RecommendationController.delete_post_by_id(recommendation_id=post_id)
