from datetime import datetime, timedelta, timezone
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
        validated_password= validate_password_strength(user.password)
        new_user= await is_new_email(user, db)
    except ValueError as e:
        logger.error(str(e))
        return {"error": str(e)}
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


def create_access_token(email: EmailStr, user_id: int, role: str, token_type: str, expires_delta: timedelta):
    encode= {"sub": email, "id": user_id, "role": role, "token_type": token_type}
    expires= datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)