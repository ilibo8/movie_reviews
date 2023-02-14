class UserInvalidPassword(Exception):
    def __init__(self, message, code=401):
        self.message = message
        self.code = code


class UserNotSuperUser(Exception):
    def __init__(self, message, code=403):
        self.message = message
        self.code = code


class UserNotFound(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


class AlreadyExist(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code
