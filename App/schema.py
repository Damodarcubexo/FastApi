from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

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