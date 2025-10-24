import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase



load_dotenv()


DB_URL= os.getenv("DB_URL")


engine= create_async_engine(DB_URL)

AsyncSessionLocal= async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit= False
)


# base call for all models
class Base(DeclarativeBase):
    pass


#database initializaztion
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 

