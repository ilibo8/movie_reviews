
class GenreNotFoundException(Exception):
    def __init__(self, message : str):
        self.message = message


class NoEntryForGenreException(Exception):
    def __init__(self, message='No data for genre.'):
        self.message = message


class GenreAlreadyExistsException(Exception):
    def __init__(self, message="Genre already in database."):
        self.message = message
