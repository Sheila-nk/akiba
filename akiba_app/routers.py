import os

from datetime import timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from . import schema, crud
from .forms import RegisterForm, LoginForm
from .database import SessionLocal

load_dotenv()

templates = Jinja2Templates(directory="akiba_app/templates")
router = APIRouter()

# Dependency
def get_db():
    """
    A single database session/connection is used for a single request
    It is closed when the request is finished
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/register/", response_class=HTMLResponse)
async def register(request: Request):
    # Display registration form
    context = {'request': request}
    return templates.TemplateResponse("register.html", context)


@router.post("/register/", response_class=HTMLResponse)
async def register_user(request: Request, db: Session = Depends(get_db)):
    # Register a new user
    form = RegisterForm(request)
    await form.load_data()
    if await form.is_valid():
        existing_user = crud.get_user_by_email(db, email=form.__dict__.get("email"))
        if not existing_user:
            new_user = schema.UserCreate(
                firstname=form.firstname,
                lastname = form.lastname,
                email=form.email,
                password=form.password
                )
            try:
                crud.create_user(db=db, user=new_user)
                return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
            except Exception as e:
                form.__dict__.get("errors").append(str(e))
                return templates.TemplateResponse("register.html", form.__dict__)
        else:
            form.__dict__.get("errors").append("User already exists!")
            return templates.TemplateResponse("register.html", form.__dict__)
    return templates.TemplateResponse("register.html", form.__dict__)


@router.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    # Display login form
    context = {'request': request}
    return templates.TemplateResponse("login.html", context)


@router.post("/login/", response_class=HTMLResponse)
async def login_user(request: Request, db: Session = Depends(get_db)):
    # Login an existing user
    form = LoginForm(request)
    await form.load_data()

    if await form.is_valid():
        existing_user = crud.get_user_by_email(db, email= form.__dict__.get("username"))
        if existing_user:
            try:
                verified_user = crud.verify_password(form.__dict__.get("password"), existing_user.hashed_pwd)
                if verified_user:
                    await login_for_access_token(form_data=form)
                    return RedirectResponse("/logout", status_code=status.HTTP_302_FOUND)
                else:
                    form.__dict__.get("errors").append("Invalid password!")
            except Exception as e:
                form.__dict__.get("errors").append(str(e))
        else:
            form.__dict__.get("errors").append("User does not exist!")
    return templates.TemplateResponse("login.html", form.__dict__)


@router.post("/token", response_model=schema.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await crud.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise credentials_exception
    access_token_expires = timedelta(minutes=int(os.environ["EXPIRATION"]))
    access_token = crud.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("logout.html", context)

""" @router.get("/logout", response_class=HTMLResponse)
def logout():
    # To be completed
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
     """