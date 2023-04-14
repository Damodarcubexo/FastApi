from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from . import utils

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "a0eead42d9fcbe6f97118cfdad1c9681819728927533b917e96a2a2aa27caaf9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: Union[str, None] = None


class User(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, name: str, password: str):
    user = utils.get_user_by_email(db, name)
    if not user:
        return False
    if not verify_password(password, get_password_hash(password)):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

