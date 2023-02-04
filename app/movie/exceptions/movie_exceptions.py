class MovieNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message


class AlreadyExistsException(Exception):
    def __init__(self, message: str):
        self.message = message
