from datetime import datetime, timedelta, timezone
from uuid import UUID
import jwt
from pydantic import EmailStr
from sqlalchemy import select
from backend.app.model.user import User
from backend.app.schema.auth_schema import CreateUserRequest
from backend.app.utils import is_new_email
from backend.app.utils.password_strength import validate_password_strength
from backend.app.core.config import SECRET_KEY, ALGORITHM
from backend.app.core.logger import logger


from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext



bcrypt_context= CryptContext(schemes= ["bcrypt"], deprecated= "auto")


async def create_user_service(user: CreateUserRequest, db: AsyncSession):
    try:
        validate_password_strength(user.password)
        existing_user= await db.scalar(select(User).where(User.email == user.email))
        if existing_user:
            raise ValueError("Email already registered")
    except ValueError as e:
        await db.rollback()
        logger.error(str(e))
        raise
    except Exception as e:
        await db.rollback()
        logger.error(str(e))
        raise
    user_request_model= User(
        email= user.email,
        hashed_password= bcrypt_context.hash(user.password),
        full_name= user.full_name,
        phone= user.phone
    )
    db.add(user_request_model)
    await db.commit()
    await db.refresh(user_request_model)



async def authenticate_user(username: str, password: str, db: AsyncSession):
     user= await db.scalar(select(User).where(User.email == username))

     if not user:
          return False
     if not bcrypt_context.verify(password, user.hashed_password):
         return False
     return user


def create_access_token(email: EmailStr, user_id, role: str, token_type: str, expires_delta: timedelta):
    encode= {"sub": email, "id": user_id, "role": role, "token_type": token_type}
    expires= datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)



async def promote_user_service(user_id: UUID, new_role:str, db: AsyncSession):
    user= await db.scalar(select(User).where(User.id == user_id))

    if not user:
        logger.error("the user doesnt exist")
        return None
    user.role= new_role
    await db.commit()
    logger.info("successfully updated the role")
    await db.refresh(user)
    return user


def refresh_access_token_service(refresh_token: str):
    payload= jwt.decode(refresh_token, SECRET_KEY, algorithms= [ALGORITHM])

    if payload.get("token_type") != "refresh":
        logger.error("invalid token type")
        return False
    email= payload.get("sub")
    user_id= payload.get("id")
    role= payload.get("role")


    new_access_token= create_access_token(email, user_id, role, "access", timedelta(minutes= 20))
    return {"access_token": new_access_token, "token_type": "bearer"} 