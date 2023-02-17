"""Module for routes for group recommendations"""
from fastapi import APIRouter, Depends
from starlette.requests import Request
from app.recommendations.schema import RecommendationSchema
from app.users.controller import JWTBearer, extract_user_id_from_token
from app.recommendations.controller import RecommendationController

recommendations_router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@recommendations_router.get("/get-all-your-posts",
                            dependencies=[Depends(JWTBearer("classic_user"))])
def get_all_your_posts(request: Request):
    user_id = extract_user_id_from_token(request)
    return RecommendationController.get_all_posts_by_user_id(user_id)


@recommendations_router.get("/get-all-posts-from-your-group",
                            dependencies=[Depends(JWTBearer("classic_user"))])
def get_all_posts_from_your_group(group_name: str, request: Request):
    user_id = extract_user_id_from_token(request)
    return RecommendationController.get_all_posts_by_group_name(group_name=group_name, user_id=user_id)


@recommendations_router.get("/get-all-posts", response_model=list[RecommendationSchema],
                            dependencies=[Depends(JWTBearer("super_user"))])
def get_all_posts():
    return RecommendationController.get_all_posts()


@recommendations_router.post("/add-post-to-your-group", dependencies=[Depends(JWTBearer("classic_user"))])
def add_post_to_your_group(group_name: str, post: str, request: Request):
    user_id = extract_user_id_from_token(request)
    return RecommendationController.add_post(group_name=group_name, user_id=user_id, post=post)


@recommendations_router.delete("/delete-post-by-its-id/{post_id}", dependencies=[Depends(JWTBearer("classic_user"))])
def delete_post_by_its_id(post_id: int, request: Request):
    user_id = extract_user_id_from_token(request)
    return RecommendationController.delete_post_by_id(recommendation_id=post_id, user_id=user_id)