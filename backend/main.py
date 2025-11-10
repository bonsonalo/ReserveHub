from fastapi import FastAPI
from contextlib import asynccontextmanager 

from backend.app.core.database import init_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app= FastAPI(title= "Booking API", lifespan= lifespan)
