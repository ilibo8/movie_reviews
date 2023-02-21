"""Module for custom exceptions for Reviews"""


class ReviewNotFound(Exception):
    def __init__(self, message : str, code=400):
        self.code = code
        self.message = message


class ReviewDuplicateEntry(Exception):
    def __init__(self, message : str, code=400):
        self.code = code
        self.message = message


class Unauthorized(Exception):
    def __init__(self, message : str, code=403):
        self.code = code
        self.message = message
