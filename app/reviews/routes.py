"""Module for Reviews routes"""
from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.movie.schema import MovieSchemaOut
from app.reviews.controller import ReviewController
from app.reviews.schema import ReviewSchema, ReviewSchemaOut, ReviewSchemaIn, \
    ReviewSchemaChangeRating, MovieAverageAndCountSchema, TopMoviesSchema
from app.users.controller import JWTBearer, extract_user_id_from_token

reviews_router = APIRouter(prefix="/api/reviews", tags=["Reviews & Ratings"])
reviews_superuser_router = APIRouter(prefix="/api/superuser/reviews", tags=["superuser - Reviews & Ratings"])


@reviews_router.get("/get-average-ratings-for-all-movies", response_model=list[MovieAverageAndCountSchema])
def get_average_ratings_for_all_movies():
    """
    Returns average rating for every movie in database.
    """
    return ReviewController.get_average_rating_and_count_for_all_movies()


@reviews_router.get("/get-average-rating-for-movie-by-title", response_model=MovieAverageAndCountSchema)
def get_average_rating_for_movie_by_title(movie_title: str):
    """
    The function accepts a movie title as an argument and returns the average rating for that movie.
    """
    return ReviewController.get_average_rating_and_count_for_movie(movie_title)


@reviews_router.get("/get-reviews-by-movie-title/{movie_title}", response_model=list[ReviewSchemaOut])
def get_reviews_by_movie_title(movie_title: str):
    """
    The function takes a movie title as an argument and returns the ratings and reviews for that movie.
    """
    return ReviewController.get_reviews_by_movie_title(movie_title)


@reviews_router.get("/get-reviews-by-user-name/{user_name}", response_model=list[ReviewSchemaOut])
def get_reviews_by_user_name(user_name: str):
    """
    The function takes in a user_name and returns all the reviews made by that user.
    """
    return ReviewController.get_reviews_by_user_name(user_name)


@reviews_router.get("/get-top-five-users-with-most-reviews")
def top_five_users_with_most_reviews():
    """
    Get list of most active users with number of their reviews.
    """
    return ReviewController.get_top_five_users_with_most_reviews()


@reviews_router.get("/get-list-of-top-rated-movies/number_of_movies_to_show", response_model=list[TopMoviesSchema])
def top_rated_movies(number_of_movies_to_show : int):
    """
    Get list of top-rated movies.
    """
    return ReviewController.get_top_n_movies_by_avg_rating(number_of_movies_to_show)


@reviews_router.get("/get-five-best-rated-movies-by-genre/{movie_genre)", response_model=list[TopMoviesSchema])
def five_best_rated_movies_by_genre(movie_genre: str):
    """
    Get list of top 5 movies by genre.
    """
    return ReviewController.get_five_best_rated_movies_by_genre(movie_genre)


@reviews_router.get("/get-all-your-reviews", response_model=list[ReviewSchemaOut],
                    dependencies=[Depends(JWTBearer("classic_user"))])
def get_all_your_reviews(request: Request):
    """
    The function is used to get all the reviews that a user has made.
    """
    user_id = extract_user_id_from_token(request)
    return ReviewController.get_personal_reviews(user_id)


@reviews_router.get("/get-not-reviewed-movie-titles", response_model=list[MovieSchemaOut],
                    dependencies=[Depends(JWTBearer("classic_user"))])
def get_list_of_movies_you_have_not_reviewed(request: Request):
    """
    Returns list of movies user hasn't reviewed.
    """
    user_id = extract_user_id_from_token(request)
    return ReviewController.get_users_not_reviewed_movies(user_id)


@reviews_router.post("/add-review", response_model=ReviewSchemaOut,
                     dependencies=[Depends(JWTBearer("classic_user"))])
def add_review(review: ReviewSchemaIn, request: Request):
    """
    The function adds a rating and review to the database.
    """
    user_id = extract_user_id_from_token(request)
    return ReviewController.add_review(movie_name=review.movie_name, user_id=user_id,
                                       rating_number=review.rating_number,
                                       review=review.review)


@reviews_router.put("/change-movie/rating-number", response_model=ReviewSchemaOut,
                    dependencies=[Depends(JWTBearer("classic_user"))])
def change_movie_rating_number(movie: ReviewSchemaChangeRating, request: Request):
    """
    The function is used to change the rating number of a movie.
    """
    user_id = extract_user_id_from_token(request)
    return ReviewController.change_movie_rating_number(movie_name=movie.movie_name, user_id=user_id,
                                                       new_rating=movie.rating_number)


@reviews_router.put("/change-movie/review", response_model=ReviewSchemaOut,
                    dependencies=[Depends(JWTBearer("classic_user"))])
def change_movie_review(movie_name: str, new_review: str, request: Request):
    """
    The function allows a user to change the review they have written for a movie.
    """
    user_id = extract_user_id_from_token(request)
    return ReviewController.change_movie_review(movie_name=movie_name, user_id=user_id, new_review=new_review)


@reviews_router.delete("/delete-personal-review", dependencies=[Depends(JWTBearer("classic_user"))])
def delete_movie_review(movie_title: str, request: Request):
    """
    The function is used to delete a review by the user who created it.
    """
    user_id = extract_user_id_from_token(request)
    return ReviewController.delete_review_by_user(movie_title, user_id)


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
