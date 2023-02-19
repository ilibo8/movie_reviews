"""Module for Reviews routes"""
from fastapi import APIRouter, Depends
from starlette.requests import Request
from app.reviews.controller import ReviewController
from app.reviews.schema import ReviewSchema, ReviewSchemaOut, ReviewWithIdSchemaOut, ReviewSchemaIn, \
    ReviewSchemaChangeRating
from app.users.controller import JWTBearer, extract_user_id_from_token
reviews_router = APIRouter(prefix="/api/reviews", tags=["Reviews & Ratings"])
reviews_superuser_router = APIRouter(prefix="/api/superuser/reviews", tags=["SuperUser - Reviews & Ratings"])


@reviews_superuser_router.get("/get-all-ratings-and-reviews", response_model=list[ReviewSchema]) #super
def get_all_reviews():
    return ReviewController.get_all_reviews()


@reviews_router.get("/get-average-ratings-for-all-movies")
def get_average_ratings_for_all_movies():
    return ReviewController.get_ratings_table()


@reviews_router.get("/get-rating-for-movie-by-name")
def get_average_rating_for_movie(movie_title: str):
    return ReviewController.get_average_rating_for_movie(movie_title)


@reviews_router.get("/get-ratings-and-reviews-by/movie-title/{movie_title}", response_model=list[ReviewSchemaOut])
def get_reviews_by_movie_title(movie_title: str):
    return ReviewController.get_reviews_by_movie_title(movie_title)


@reviews_router.get("/get-ratings-and-reviews-by/user-name/{user_name}", response_model=list[ReviewSchemaOut])
def get_reviews_by_user_name(user_name: str):
    return ReviewController.get_reviews_by_user_name(user_name)


@reviews_router.get("/get-personal-reviews-info", response_model=list[ReviewWithIdSchemaOut],
                    dependencies=[Depends(JWTBearer("classic_user"))])
def get_personal_reviews_info(request : Request):
    user_id = extract_user_id_from_token(request)
    return ReviewController.get_personal_reviews(user_id)


@reviews_router.post("/add-rating-and-review", response_model=ReviewSchemaOut,
                     dependencies=[Depends(JWTBearer("classic_user"))])
def add_rating_and_review(review : ReviewSchemaIn, request : Request):
    user_id = extract_user_id_from_token(request)
    return ReviewController.add_review(movie_name=review.movie_name, user_id=user_id,
                                       rating_number=review.rating_number,
                                       review=review.review)


@reviews_router.put("/change-movie/rating-number", response_model=ReviewSchemaOut,
                    dependencies=[Depends(JWTBearer("classic_user"))])
def change_movie_rating_number(movie: ReviewSchemaChangeRating, request : Request):
    user_id = extract_user_id_from_token(request)
    return ReviewController.change_movie_rating_number(movie_name=movie.movie_name, user_id=user_id,
                                                       new_rating=movie.rating_number)


@reviews_router.put("/change-movie/review", response_model=ReviewSchemaOut,
                    dependencies=[Depends(JWTBearer("classic_user"))])
def change_movie_review(movie_name: str, new_review: str, request : Request):
    user_id = extract_user_id_from_token(request)
    return ReviewController.change_movie_review(movie_name=movie_name, user_id=user_id, new_review=new_review)


@reviews_router.delete("/delete-personal-review", dependencies=[Depends(JWTBearer("classic_user"))])
def delete_review_by_id(review_id: int, request : Request):
    user_id = extract_user_id_from_token(request)
    return ReviewController.delete_review_id_by_user(review_id, user_id)


@reviews_superuser_router.delete("/delete-review-by-id")#, dependencies=[Depends(JWTBearer("super_user"))])
def delete_review_by_id(review_id):
    return ReviewController.delete_review_by_id(review_id)
