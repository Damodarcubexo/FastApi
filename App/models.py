from .database import Base
from sqlalchemy import Column, Integer, String, Enum
from .schema import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(Enum(UserRole, name= 'role'), default=UserRole.user)
    phone_number = Column(String)
    otp = Column(String, nullable=True)
