"""Module for Reviews service"""
from app.db import SessionLocal
from app.genre.exceptions import GenreNotFound
from app.genre.repository import GenreRepository
from app.movie.exceptions import MovieNotFound
from app.movie.repository import MovieRepository
from app.reviews.repository import ReviewRepository
from app.reviews.exceptions import ReviewNotFound, Unauthorized, ReviewDuplicateEntry
from app.users.repository import UserRepository


class ReviewService:
    """Class for Review service layer"""

    @staticmethod
    def add_review(movie_name: str, user_id: int, rating_number: int, review: str):
        """
        The add_review function adds a review to the database.
        rating number is an integer between 1 and 10 inclusive which represents how much you liked/disliked this
        particular movie out of ten (10 being most liked).
        review is a string containing your opinion about this particular film.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_name)
                review = review_repository.add_review(movie_id=movie_id, user_id=user_id, rating_number=rating_number,
                                                      review=review)
                return review
        except ReviewDuplicateEntry as err:
            raise err
        except Exception as err:
            raise err

    @staticmethod
    def get_all_reviews():
        """
        The function returns all reviews in the database.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                return review_repository.get_all_reviews()
        except Exception as err:
            raise err

    @staticmethod
    def get_review_by_id(review_id: int):
        """
        The function returns review by its id.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                review = review_repository.get_review_by_id(review_id)
                if review is None:
                    raise ReviewNotFound(f"There is no review with id {review_id}")
                return review
        except Exception as err:
            raise err

    @staticmethod
    def get_all_reviews_for_users():
        """
        The get_all_reviews function returns all reviews in the database.
        """
        try:
            with SessionLocal() as db:
                movie_repository = MovieRepository(db)
                movies = movie_repository.get_all_movies_order_by_name()
                return movies
        except Exception as err:
            raise err

    @staticmethod
    def get_average_rating_for_movie(movie_title: str):
        """
        The get_average_rating_for_movie function takes a movie title as an argument and returns the average
        rating for that movie. It first retrieves the Movie ID from the database using get_movie_id_by_title,
        then uses get_average_rating to retrieve the average rating and number of ratings for that movie.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_title)
                if len(review_repository.get_reviews_by_movie_id(movie_id)) == 0:
                    raise ReviewNotFound(f"There are no reviews for movie {movie_title}")
                rating_and_count = review_repository.get_average_rating_and_count_by_movie_id(movie_id)
                movie = movie_repository.get_movie_by_id(movie_id)
                movie.average_rating = rating_and_count[0]
                movie.number_of_ratings = rating_and_count[1]
                if movie.number_of_ratings == 0:
                    raise ReviewNotFound("There are no ratings for this movie yet.")
                return movie
        except Exception as err:
            raise err

    @staticmethod
    def get_movies_rating_between(bottom_rating: int, top_rating: int):
        """
        The function accepts a movie title as an argument and returns the average rating for that movie.
        """
        try:
            with SessionLocal() as db:
                if bottom_rating >= top_rating or bottom_rating not in range(1, 11) or top_rating not in range(1, 11):
                    raise ValueError
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                all_movies = movie_repository.get_all_movies_order_by_name()
                movies_in_range = []
                for movie in all_movies:
                    movie.average_rating = review_repository.get_average_rating_and_count_by_movie_id(movie.id)[0]
                    movie.number_of_ratings = review_repository.get_average_rating_and_count_by_movie_id(movie.id)[1]
                    if bottom_rating <= movie.average_rating <= top_rating:
                        movies_in_range.append(movie)
                if len(movies_in_range) == 0:
                    raise MovieNotFound("There are no movies with this range")
                return movies_in_range
        except Exception as err:
            raise err

    @staticmethod
    def get_reviews_by_movie_title(movie_title: str):
        """
        The get_reviews_by_movie_title function takes a movie title as an argument and returns all the reviews for
        that movie. If there are no reviews for that movie, it will return an error message.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_title)
                reviews = review_repository.get_reviews_by_movie_id(movie_id)
                if len(reviews) == 0:
                    raise ReviewNotFound(f"There is no review for movie {movie_title}.")
                return reviews
        except Exception as err:
            raise err

    @staticmethod
    def get_reviews_by_user_name(user_name: str):
        """
        The get_reviews_by_user_name function takes a user_name as an argument and returns all the reviews
        written by that user. If no review is found, it raises a ReviewNotFound exception.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                user_repository = UserRepository(db)
                user = user_repository.get_user_by_user_name(user_name)
                reviews = review_repository.get_reviews_by_user_id(user.id)
                if len(reviews) == 0:
                    raise ReviewNotFound(f"User {user_name} didn't post any reviews yet.")
                return reviews
        except Exception as err:
            raise err

    @staticmethod
    def get_personal_reviews(user_id: int):
        """
        The get_personal_reviews function retrieves all the reviews that a user has created.
        It takes in an integer as input and returns a list of dictionaries, where each dictionary contains
        information about one review.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                reviews = review_repository.get_reviews_by_user_id(user_id)
                if len(reviews) == 0:
                    raise ReviewNotFound("You don't have reviews yet.")
                return reviews
        except Exception as err:
            raise err

    @staticmethod
    def get_top_five_users_with_most_reviews():
        """
        Get list of most active users with number of their reviews.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                user_repository = UserRepository(db)
                users = review_repository.get_top_five_users_with_most_reviews()
                users_reformatted = []
                for count, user in enumerate(users):
                    user_name = user_repository.get_user_name_by_user_id(user[0])
                    users_reformatted.append({f"No. {count + 1}": user_name, "number_of_ratings": user[1]})
                return users_reformatted
        except Exception as err:
            raise err

    @staticmethod
    def get_top_n_movies_by_avg_rating(top: int):
        """
        Get list of top n movies by average rating
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movies = movie_repository.get_all_movies()
                if top > len(movies) or top <= 0:
                    raise ValueError("Must be positive number.")
                movies_tuple = review_repository.get_top_n_movies_by_avg_rating(top)
                movies = []
                for count, movie in enumerate(movies_tuple):
                    movie_obj = movie_repository.get_movie_by_id(movie[0])
                    movie_obj.average_rating = movie[1]
                    movie_obj.number_of_ratings = movie[2]
                    movies.append({"rank": count + 1, "movie": movie_obj})
                return movies
        except Exception as err:
            raise err

    @staticmethod
    def get_five_best_rated_movies_by_genre(genre: str):
        """
        Returns top n movies of certain genre by their average rating.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                genre_repository = GenreRepository(db)
                if genre_repository.check_is_there(genre) is False:
                    raise GenreNotFound(f"There is no genre named {genre}")
                movies_tuple = review_repository.get_five_best_rated_movies_by_genre(genre)
                movies = []
                for count, movie in enumerate(movies_tuple):
                    movie_obj = movie_repository.get_movie_by_id(movie[0])
                    movie_obj.average_rating = movie[1]
                    movie_obj.number_of_ratings = movie[2]
                    movies.append({"rank": count + 1, "movie": movie_obj})
                return movies
        except Exception as err:
            raise err

    @staticmethod
    def get_users_not_reviewed_movies(user_id: int):
        """
        Returns list of movies user hasn't reviewed.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movies_repository = MovieRepository(db)
                reviews = review_repository.get_reviews_by_user_id(user_id)
                movies = movies_repository.get_all_movies()
                all_movies_ids = [movie.id for movie in movies]
                user_reviewed_movie_ids = [review.movie_id for review in reviews]
                unreviewed = set(all_movies_ids).difference(set(user_reviewed_movie_ids))
                unreviewed_movies = [movies_repository.get_movie_by_id(m_id) for m_id in unreviewed]
                if len(unreviewed_movies) == 0:
                    raise ReviewNotFound("You've reviewed all movies.")
                return unreviewed_movies
        except Exception as err:
            raise err

    @staticmethod
    def change_movie_rating_number(movie_name: str, user_id: int, new_rating: int):
        """
        The change_movie_rating_number function allows a user to change the rating of a movie they have previously
        rated.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_name)
                review = review_repository.change_movie_rating(movie_id, user_id, new_rating)
                return review
        except Exception as err:
            raise err

    @staticmethod
    def change_movie_review(movie_name: str, user_id: int, new_review: str):
        """
        The change_movie_review function allows a user to change the review they have written for a movie.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_name)
                review = review_repository.change_movie_review(movie_id, user_id, new_review)
                return review
        except Exception as err:
            raise err

    @staticmethod
    def delete_review_by_user(movie_title: str, user_id: int):
        """
        The delete_review_id_by_user function deletes a review by the user's id.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                movie_repository = MovieRepository(db)
                movie_id = movie_repository.get_movie_id_by_title(movie_title)
                review = review_repository.get_reviews_by_user_id_and_movie_id(movie_id=movie_id, user_id=user_id)
                if review is None:
                    raise ReviewNotFound("You don't have review for this movie.")
                review = review_repository.delete_review_by_id(review.id)
                if review:
                    return review
        except ReviewNotFound as err:
            raise err
        except Unauthorized as err:
            raise err
        except Exception as err:
            raise err

    @staticmethod
    def delete_review_by_id(review_id: int):
        """
        The delete_review_by_id function deletes a review from the database by its id.
        It takes in an integer as an argument and returns True if it is successful.
        """
        try:
            with SessionLocal() as db:
                review_repository = ReviewRepository(db)
                if review_repository.delete_review_by_id(review_id):
                    return True
        except ReviewNotFound as err:
            raise err
        except Exception as err:
            raise err
