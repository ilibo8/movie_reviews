class NotFoundException(Exception):
    def __init__(self, message: str, code=400):
        self.message = message
        self.code = code


class DuplicateDataEntryException(Exception):
    def __init__(self, message: str, code=400):
        self.message = message
        self.code = code
