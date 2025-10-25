from backend.app.core.database import AsyncSessionLocal


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db