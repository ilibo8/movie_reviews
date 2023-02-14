from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.users.service import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, role: str, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.role = role

    async def __call__(self, request: Request):
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
                    detail="User with provided role is not permitted to access this " "route.",
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> dict:
        is_token_valid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return {"valid": is_token_valid, "role": payload["role"]}
