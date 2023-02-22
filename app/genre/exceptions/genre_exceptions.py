"""Module for Genre custom exceptions"""


class GenreNotFound(Exception):
    def __init__(self, message : str):
        self.message = message


class NoEntryForGenre(Exception):
    def __init__(self, message='No data for genre.'):
        self.message = message


class GenreAlreadyExists(Exception):
    def __init__(self, message="Genre already in database."):
        self.message = message
