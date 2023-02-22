"""Module for Recommendations custom exceptions"""


class RecommendationNotFound(Exception):
    def __init__(self, message: str, code=404):
        self.message = message
        self.code = code


class Unauthorized(Exception):
    def __init__(self, message: str, code=403):
        self.message = message
        self.code = code
