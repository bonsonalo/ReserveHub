from datetime import timedelta
from fastapi import Depends, FastAPI, APIRouter, HTTPException
from sqlalchemy import select
from starlette import status
from passlib.context import CryptContext
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.schema.auth_schema import CreateUserRequest, Token
from backend.app.core.config import db_dependency
from backend.app.service.auth_service import create_access_token, create_user_service, authenticate_user
from backend.app.utils.password_strength import validate_password_strength
from backend.app.model.user import User
from backend.app.core.logger import logger



router = APIRouter(
    prefix= "/auth",
    tags= "auth"
)


# bcrypt_context= CryptContext(schemes= ["bcrypt"], deprecated= "auto")

# sign up
@router.post("/signup", status_code= status.HTTP_201_CREATED)
async def create_user(user: CreateUserRequest, db: db_dependency):
    try:
         logger.info("going to create user")
         return await create_user_service(user, db)
    except ValueError as e:
         logger.error(str(e))
         raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "password should include uppercase letter, lowercase letter, special letter and number")


# for login

@router.get("/login", status_code=status.HTTP_200_OK)
async def login_for_access_token(user_form: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
     user= await authenticate_user(user_form.username, user_form.password, db)
     if not user:
          logger.error("could not login into account")
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
     access_token= create_access_token(user.email, user.id, user.role, "access", timedelta(minutes=20))
     refresh_token= create_access_token(user.email, user.id, user.role, "refresh", timedelta(days=30))

     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}






          




