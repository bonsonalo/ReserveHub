from fastapi import FastAPI

from backend.app.core.database import init_db



app= FastAPI(title= "Booking API")





@app.lifespan("startup")
async def on_startup():
    await init_db()

