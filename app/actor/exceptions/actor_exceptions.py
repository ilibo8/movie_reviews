class ActorNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message


class NoDataFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
