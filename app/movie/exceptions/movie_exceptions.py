class MovieNotFound(Exception):
    def __init__(self, message: str, code=400):
        self.message = message
        self.code = code


class DuplicateDataEntry(Exception):
    def __init__(self, message: str, code=400):
        self.message = message
        self.code = code
