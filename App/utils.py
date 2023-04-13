from .models import User
from . import database


def get_user_by_email(db: database.SessionLocal, name: str):
    return db.query(User).filter(User.name == name).first()
