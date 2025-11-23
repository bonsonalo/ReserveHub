from fastapi import FastAPI
from contextlib import asynccontextmanager 
from mangum import Mangum

from backend.app.core.database import init_db
from backend.app.api.v1.routes import routers



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app= FastAPI(title= "Booking API", lifespan= lifespan)
app.include_router(routers)

handler= Mangum(app)