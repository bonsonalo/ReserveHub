from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import os



from backend.app.core.database import AsyncSessionLocal



load_dotenv()


SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM= os.getenv("ALGORITHM")




async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

    
db_dependency= Annotated[AsyncSession, Depends(get_db)]
