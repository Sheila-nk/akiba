import os

from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from uuid import uuid4
from sqlalchemy.orm import Session

from . import schema, model


load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(password, hashed_pwd):
    return pwd_context.verify(password, hashed_pwd)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_uuid():
    return uuid4().hex

def create_user(db: Session, user: schema.UserCreate):
    # Create a new user
    hashed_pwd = get_password_hash(user.password)

    new_user = model.User(
        firstname=user.firstname, 
        lastname=user.lastname, 
        email=user.email,
        hashed_pwd = hashed_pwd,
        id=get_uuid(),
        registered_on=datetime.now()
        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=os.environ("EXPIRATION"))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        os.environ["SECRET_KEY"], 
        algorithm=os.environ["ALGORITHM"]
        )
    return encoded_jwt
    

async def authenticate_user(username: str, password: str, db: Session):
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_pwd):
        return False
    return user


""" async def get_current_user(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user
 """

# def blacklist_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
"""
need to create a Blacklisted Token model
when a user logs out, the token is added to the table
also create a decode token function
"""