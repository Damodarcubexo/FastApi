from fastapi import Depends, Header, HTTPException
from jwt import decode, InvalidTokenError
from . import role_and_perms
from typing import List

SECRET_KEY = "a0eead42d9fcbe6f97118cfdad1c9681819728927533b917e96a2a2aa27caaf9"

async def get_user_roles(authorization: str = Header(...)) -> List[role_and_perms.Role]:
    try:
        token = authorization.split(" ")[1]
        payload = decode(token, SECRET_KEY, algorithms=["HS256"])
        user_roles = [role_and_perms.Role(role) for role in payload.get("roles", [])]
        return user_roles
    except (IndexError, InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token or missing roles")
