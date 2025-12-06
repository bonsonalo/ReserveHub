from datetime import timedelta
from uuid import UUID
from fastapi import BackgroundTasks, Depends, APIRouter, HTTPException

from starlette import status
from passlib.context import CryptContext
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from jose import ExpiredSignatureError, JWTError


from backend.app.schema.auth_schema import CreateUserRequest, RefreshTokenRequest, Token
from backend.app.core.config import db_dependency, superadmin_dependency
from backend.app.service.auth_service import create_access_token, create_user_service, authenticate_user, promote_user_service, refresh_access_token_service
from backend.app.core.logger import logger



router = APIRouter(
    prefix= "/api/v1/auth",
    tags= ["auth"]
)



# sign up
@router.post("/signup", status_code= status.HTTP_201_CREATED)
async def create_user(user: CreateUserRequest, bg_task: BackgroundTasks, db: db_dependency):
    try:
         logger.info("going to create user")
         return await create_user_service(user, bg_task, db)
    except ValueError as e:
         logger.error(str(e))
         raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= str(e))


# for login

@router.get("/login", status_code=status.HTTP_200_OK)
async def login_for_access_token(user_form: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
     user= await authenticate_user(user_form.username, user_form.password, db)
     if not user:
          logger.error("could not login into account")
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
     access_token= create_access_token(user.email, str(user.id), user.role, "access", timedelta(minutes=20))
     refresh_token= create_access_token(user.email, str(user.id), user.role, "refresh", timedelta(days=30))

     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# to upgrade user

@router.put("/promote/{user_id}")
async def promote_user(user_id: UUID, new_role: str, db: db_dependency, current_user: superadmin_dependency):
     updated= await promote_user_service(user_id, new_role, db)
     if not updated:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "user not found")
     return updated


# refresh

@router.post("/refresh")
async def refresh_access_token(request: RefreshTokenRequest):
     try:
          return refresh_access_token_service(request.refresh_token)
     except ExpiredSignatureError:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token expired")
     except JWTError:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "invalid refresh token")

     





          




