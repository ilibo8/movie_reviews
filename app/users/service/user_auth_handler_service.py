"""Module for user authentication and authorization service."""
import time
from typing import Dict
import jwt
from app.config import settings

USER_SECRET = settings.USER_SECRET
JWT_ALGORITHM = settings.ALGORITHM


def sign_JWT(user_id: str, role: str) -> Dict[str, str]:
    """
    The sign_JWT function signs a JWT token with the user's ID and role.
    It returns a dictionary containing the access_token, which is used to authenticate
    the user when they make requests to protected endpoints.
    """
    payload = {"user_id": user_id, "role": role, "expires": time.time() + 1500}
    token = jwt.encode(payload, USER_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token": token}


def decode_JWT(token: str) -> dict:
    """
    The decode_JWT function takes a JWT token as an argument and returns the decoded
    JWT payload if the token is valid, or None if it is not. The function also checks that
    the expiration time of the JWT has not passed.
    """
    try:
        decoded_token = jwt.decode(token, USER_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
