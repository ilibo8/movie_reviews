"""Module for Exceptions for Users"""


class UserInvalidPassword(Exception):
    """Raise when user password is incorrect."""
    def __init__(self, message, code=401):
        self.message = message
        self.code = code


class UserNotSuperUser(Exception):
    """Raise when user is not super_user."""
    def __init__(self, message, code=403):
        self.message = message
        self.code = code


class UserNotFound(Exception):
    """Raise when user object is not found."""
    def __init__(self, message, code=404):
        self.message = message
        self.code = code


class AlreadyExist(Exception):
    """Raise when attempting to add data than already exist."""
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


class TokenExpired(Exception):
    """Raise when token expires."""
    def __init__(self, message="Token expired.", code=401):
        self.message = message
        self.code = code
