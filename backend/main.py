from fastapi import FastAPI
from contextlib import asynccontextmanager 
from mangum import Mangum
from redis import Redis
import httpx

from backend.app.core.database import init_db
from backend.app.api.v1.routes import routers
from backend.app.core.middleware import register_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.redis= Redis(host= 'localhost', port= 6379)
    app.state.http_client= httpx.AsyncClient()
    yield
    app.state.redis.close()


app= FastAPI(title= "Booking API", lifespan= lifespan)

register_middleware(app)


app.include_router(routers)

handler= Mangum(app)