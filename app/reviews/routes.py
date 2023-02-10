from fastapi import APIRouter

from app.reviews.controller import ReviewController
from app.reviews.schema import ReviewSchema, ReviewSchemaIn

reviews_router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


@reviews_router.get("get-all-reviews", response_model=list[ReviewSchema])
def get_all_reviews():
    return ReviewController.get_all_reviews()


@reviews_router.get("get-reviews-by/movie-id/{movie_id}", response_model=list[ReviewSchema])
def get_reviews_by_movie_id(movie_id: int):
    return ReviewController.get_reviews_by_movie_id(movie_id)


@reviews_router.get("get-reviews-by/user-id/{user_id}", response_model=list[ReviewSchema])
def get_reviews_by_user_id(user_id: str):
    return ReviewController.get_reviews_by_user_id(user_id)


@reviews_router.post("/add-review", response_model=ReviewSchema)
def add_review(review : ReviewSchemaIn):
    return ReviewController.add_review(movie_id=review.movie_id, user_id=review.user_id,
                                       rating_number=review.rating_number,
                                       rating_description=review.rating_description)


@reviews_router.put("change-movie/rating-number", response_model=ReviewSchema)
def change_movie_rating_number(movie_id: int, user_id: str, new_rating: int):
    return ReviewController.change_movie_rating_number(movie_id, user_id, new_rating)


@reviews_router.put("change-movie/rating-description", response_model=ReviewSchema)
def change_movie_rating_description(movie_id: int, user_id: str, new_description: str):
    return ReviewController.change_movie_rating_description(movie_id, user_id, new_description)


@reviews_router.delete("/delete-review")
def delete_review_by_id(review_id: int):
    return ReviewController.delete_review_by_id(review_id)

