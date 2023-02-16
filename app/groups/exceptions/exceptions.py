class GroupNotFound(Exception):
    def __init__(self, message: str, code=400):
        self.code = code
        self.message = message


class GroupUserNotFound(Exception):
    def __init__(self, message: str, code=400):
        self.code = code
        self.message = message


class DuplicateEntry(Exception):
    def __init__(self, message: str, code=400):
        self.code = code
        self.message = message


class Unauthorized(Exception):
    def __init__(self, message: str, code=403):
        self.code = code
        self.message = message
