from fastapi import Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status


from backend.app.core.database import AsyncSessionLocal
from backend.app.core.logger import logger


load_dotenv()


SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM= os.getenv("ALGORITHM")




async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

    
db_dependency= Annotated[AsyncSession, Depends(get_db)]

oauth_bearer= OAuth2PasswordBearer(tokenUrl= "auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        email:str= payload.get("sub")
        user_id: int= payload.get("id")
        role: str= payload.get("role")

        if email is None or user_id is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Could not be validated")
        return {"email": email, "id": user_id, "role": role}
    except JWTError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= str(e))
    

user_authentication_dependency= Annotated[dict, Depends(get_current_user)]


def role_required(allowed_roles: List[str]):
    def wrapper(current_user: user_authentication_dependency):
        user_role= current_user.get("role")
        if not user_role:
            logger.error("There is no role assigned")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "user has no roles assigned")
        if user_role not in allowed_roles:
            logger.error("you are not authorized to access")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "you are not authorized to access")
        return current_user
    return wrapper



user_dependency= Annotated[dict, Depends(role_required(["user", "admin", "superadmin"]))]
admin_dependency= Annotated[dict, Depends(role_required(["admin", "superadmin"]))]
superadmin_dependency= Annotated[dict, Depends(role_required(["superadmin"]))]
