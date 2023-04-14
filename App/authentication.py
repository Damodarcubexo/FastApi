from fastapi import Depends, Header, HTTPException
from jwt import decode, InvalidTokenError
from . import schema
from typing import List
from . auth_token import SECRET_KEY


async def get_user_roles(authorization: str = Header(...)) -> List[schema.UserRole]:
    try:
        token = authorization.split(" ")[1]
        payload = decode(token, SECRET_KEY, algorithms=["HS256"])
        user_roles = [schema.UserRole(role) for role in payload.get("role", [])]
        return user_roles
    except (IndexError, InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token or missing roles")
