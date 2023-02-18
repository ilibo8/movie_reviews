"""Module for Genre Repository"""
from sqlalchemy.orm import Session
from app.genre.exceptions import GenreNotFound
from app.genre.model import Genre


class GenreRepository:
    """Class for Genre repository layer."""
    def __init__(self, db: Session):
        self.db = db

    def add_genre(self, name: str):
        """
        The add_genre function creates a new Genre object and adds it to the database.
        It then returns the newly created genre.

        :param self: Access the database connection
        :param name:str: Set the name of the genre
        :return: The genre object that was created
        """
        genre = Genre(name)
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre

    def get_all_genres(self):
        """
        The get_all_genres function returns a list of all the genres in the database.

        :param self: Refer to the class instance
        :return: A list of all the genres in the database
        """
        return self.db.query(Genre).all()

    def check_is_there(self, name) -> bool:
        """
        The check_is_there function checks if the genre name is already in the database.
        If it is, then it returns True. If not, then it returns False.

        :param self: Access the attributes and methods of the class
        :param name: Check if the name is already in the database
        :return: True if the genre name is already in the database, and false otherwise
        """
        if self.db.query(Genre).filter(Genre.name == name).first() is None:
            return False
        return True

    def delete(self, name: str):
        """
        The delete function takes a name as an argument and deletes the genre with that name from the database.
        If no such genre exists, it raises a GenreNotFound exception.

        :param self: Access the attributes and methods of the class
        :param name:str: Specify the name of the genre to be deleted
        :return: True
        """
        genre = self.db.query(Genre).filter(Genre.name == name).first()
        if genre is None:
            raise GenreNotFound(f"There is no {name} entry.")
        self.db.delete(genre)
        self.db.commit()
        return True
