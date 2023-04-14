from fastapi import FastAPI, HTTPException, status
from .utils import get_user_by_email
from . import database
from .models import User
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from . import auth_token
from .sms_send import Client, TWILIO_ACCOUNT_SID, TWILIO_PHONE_NUMBER, TWILIO_AUTH_TOKEN
import random
from fastapi import APIRouter, Depends
from . import authentication
from typing import List
from fastapi import HTTPException
from .import schema
app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)


router = APIRouter()

@app.post("/users", response_model=User)
async def create_user(user: auth_token.User):
    db = database.SessionLocal()
    db_user = get_user_by_email(db, name=user.name)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this Name already registered",
        )
    otp = str(random.randint(100000, 999999))
    # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    # message = client.messages.create(
    #     body=f'Your OTP is: {otp}',
    #     from_=TWILIO_PHONE_NUMBER,
    #     to=user.phone_number
    # )
    db_user = User(name=user.name,email=user.email,password=user.password, phone_number=user.phone_number, otp= otp)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        # "message": message.__dict__['body']+" "+"Please enter thcreate_engineis otp to activate your account",
        "user_id": db_user.id,
        "status_code": status.HTTP_201_CREATED,
    }

@app.get("/users/{user_id}")
async def read_user(user_id: int,user_roles: List[schema.UserRole] = Depends(authentication.get_user_roles)):
    db = database.SessionLocal()
    if user_roles =='admin':
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            return {"id": db_user.id, "name": db_user.name, "email": db_user.email}
        else:
            return {"message": "User not found"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not authorise to access this route!!",
        )


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: auth_token.User):
    db = database.SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        db_user.password = user.password
        db.commit()
        return {"message": "User updated successfully!"}
    else:
        return {"message": "User not found"}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    db = database.SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully!"}
    else:
        return {"message": "User not found"}


@app.post("/token", response_model=auth_token.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    db = database.SessionLocal()
    user = auth_token.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_token.create_access_token(
        data={"sub": user.name, "role":schema.UserRole}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/verify-otp")
async def verify_otp(otp:str):
    db = database.SessionLocal()
    db_user = db.query(User).filter(User.otp == otp).first()
    if db_user:
        db_user.otp = None
        db.commit()
        return {"message": "User registered successfully!"}
    else:
        return {"message": "Invalid otp, Please enter the correct one!!!"}

