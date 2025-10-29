from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession




from backend.app.model.user import User
from backend.app.schema.auth_schema import CreateUserRequest


async def is_new_email(user_data: CreateUserRequest, db: AsyncSession):
    existing_user= await db.scalar(select(User).where(User.email == user_data.email))
    if existing_user:
        raise ValueError("the email already exists")
    return True