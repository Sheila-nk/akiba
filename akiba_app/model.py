# SQLAlchemy models

from sqlalchemy import Column, String, DateTime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, nullable = False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_pwd = Column(String, nullable=False)
    registered_on = Column(DateTime, nullable=False)