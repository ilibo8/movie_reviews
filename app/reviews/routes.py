"""Module for Reviews routes"""
from fastapi import APIRouter, Depends
from starlette.requests import Request
from app.reviews.controller import ReviewController
from app.reviews.schema import ReviewSchema, ReviewSchemaOut, ReviewWithIdSchemaOut, ReviewSchemaIn, \
    ReviewSchemaChangeRating
from app.users.controller import JWTBearer, extract_user_id_from_token

reviews_router = APIRouter(prefix="/api/reviews", tags=["Reviews & Ratings"])
reviews_superuser_router = APIRouter(prefix="/api/superuser/reviews", tags=["superuser - Reviews & Ratings"])


@reviews_router.get("/get-average-ratings-for-all-movies")
def get_average_ratings_for_all_movies():
    """
    Returns 'average' (the average rating for that movie) and 'total_ratings'
    (the total number of ratings for that movie) for every movie in database.
    """
    return ReviewController.get_ratings_table()


@reviews_router.get("/get-rating-for-movie-by-title")
def get_average_rating_for_movie_by_title(movie_title: str):
    """
    The function accepts a movie title as an argument and returns the average rating for that movie.
    """
    return ReviewController.get_average_rating_for_movie(movie_title)


@reviews_router.get("/get-ratings-and-reviews-by/movie-title/{movie_title}", response_model=list[ReviewSchemaOut])
def get_ratings_and_reviews_by_movie_title(movie_title: str):
    """
    The function takes a movie title as an argument and returns the ratings and reviews for that movie.
    """
    return ReviewController.get_reviews_by_movie_title(movie_title)


@reviews_router.get("/get-ratings-and-reviews-by/user-name/{user_name}", response_model=list[ReviewSchemaOut])
def get_ratings_and_reviews_by_user_name(user_name: str):
    """
    The function takes in a user_name and returns all the reviews made by that user.
    """
    return ReviewController.get_reviews_by_user_name(user_name)


@reviews_router.get("/get-personal-reviews-info", response_model=list[ReviewWithIdSchemaOut],
                    dependencies=[Depends(JWTBearer("classic_user"))])
def get_personal_reviews_info(request : Request):
    """
    The is used to get all the reviews that a user has made.
    """
    user_id = extract_user_id_from_token(request)
    return ReviewController.get_personal_reviews(user_id)


@reviews_router.post("/add-rating-and-review", response_model=ReviewSchemaOut,
                     dependencies=[Depends(JWTBearer("classic_user"))])
def add_rating_and_review(review : ReviewSchemaIn, request : Request):
    """
    The function adds a rating and review to the database.
    """
    user_id = extract_user_id_from_token(request)
    return ReviewController.add_review(movie_name=review.movie_name, user_id=user_id,
                                       rating_number=review.rating_number,
                                       review=review.review)


@reviews_router.put("/change-movie/rating-number", response_model=ReviewSchemaOut,
                    dependencies=[Depends(JWTBearer("classic_user"))])
def change_movie_rating_number(movie: ReviewSchemaChangeRating, request : Request):
    """
    The function is used to change the rating number of a movie.
    """
    user_id = extract_user_id_from_token(request)
    return ReviewController.change_movie_rating_number(movie_name=movie.movie_name, user_id=user_id,
                                                       new_rating=movie.rating_number)


@reviews_router.put("/change-movie/review", response_model=ReviewSchemaOut,
                    dependencies=[Depends(JWTBearer("classic_user"))])
def change_movie_review(movie_name: str, new_review: str, request : Request):
    """
    The function allows a user to change the review they have written for a movie.
    """
    user_id = extract_user_id_from_token(request)
    return ReviewController.change_movie_review(movie_name=movie_name, user_id=user_id, new_review=new_review)


@reviews_router.delete("/delete-personal-review", dependencies=[Depends(JWTBearer("classic_user"))])
def delete_review_by_id(review_id: int, request : Request):
    """
    The function is used to delete a review by the user who created it.
    """
    user_id = extract_user_id_from_token(request)
    return ReviewController.delete_review_id_by_user(review_id, user_id)


@reviews_superuser_router.get("/get-all-ratings-and-reviews", response_model=list[ReviewSchema],
                              dependencies=[Depends(JWTBearer("super_user"))])
def get_all_reviews():
    """
    The function returns a list of all reviews in the database.
    """
    return ReviewController.get_all_reviews()


@reviews_superuser_router.delete("/delete-review-by-id", dependencies=[Depends(JWTBearer("super_user"))])
def delete_review_by_id(review_id):
    """
    The function deletes a review from the database.
    """
    return ReviewController.delete_review_by_id(review_id)
