"""Module for JWTBearer"""
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.users.service import decodeJWT


def extract_user_id_from_token(request: Request) -> int:
    """Function for extracting user id from authorised request."""
    bearer = request.headers["authorization"]
    token = bearer.split()[1]
    decoded = decodeJWT(token)
    user_id = decoded["user_id"]
    return user_id



class JWTBearer(HTTPBearer):
    """Class for checking credentials."""
    def __init__(self, role: str, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.role = role

    async def __call__(self, request: Request):
        """Method for checking credentials."""
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            payload = self.verify_jwt(credentials.credentials)
            if not payload.get("valid"):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            if payload.get("role") != self.role:
                raise HTTPException(
                    status_code=403,
                    detail="User with provided role is not permitted to access this route.",
                )
            return credentials.credentials
        raise HTTPException(status_code=403, detail="Invalid authorization code.")


    @staticmethod
    def verify_jwt(jwt_token: str) -> dict:
        try:
            payload = decodeJWT(jwt_token)
        except Exception as e:
            print(e)
            payload = None
        return {"valid": bool(payload), "role": payload["role"] if payload else None}
