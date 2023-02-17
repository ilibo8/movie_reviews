
class ReviewNotFound(Exception):
    def __init__(self, message : str, code=400):
        self.code = code
        self.message = message


class ReviewDuplicateEntry(Exception):
    def __init__(self, message : str, code=400):
        self.code = code
        self.message = message
