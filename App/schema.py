from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    user = 'user'
    admin = 'admin'


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole

class UserRead(BaseModel):
    id: int
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str
    email: str
    password: str

class UserDelete(BaseModel):
    id: int