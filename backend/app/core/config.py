from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession




from backend.app.core.database import AsyncSessionLocal








async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

    
db_dependency= Annotated[AsyncSession, Depends(get_db)]