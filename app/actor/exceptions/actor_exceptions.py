"""Module for Exceptions for Actor."""


class ActorNotFound(Exception):
    """Exception when object Actor is not found."""
    def __init__(self, message: str):
        self.message = message

