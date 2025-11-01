from sqlalchemy import select, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.model.user import User
from backend.app.core.logger import logger
from backend.app.schema import user_schema





async def get_users_schema(db: AsyncSession):
    user= await db.scalars(select(User))

    if not user:
        logger.error("user not found")
        raise LookupError("user not found")
    logger.info("successfully displayed the user")
    return user


async def get_user_info_service(user_id: UUID, db: AsyncSession):
    user= await db.scalar(select(User).where(User.id == user_id, User.archived == False))
    if not user:
        raise ValueError("No user with that username")
    return user



async def update_user_service(id: UUID, user_update: user_schema.UpdateUser, db: AsyncSession):
    user= db.scalar(select(User).where(User.id == id))
    if not user:
        raise LookupError("Couldnot find the user with that id")
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.phone is not None:
        user.phone = user_update.phone

    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_id_service(id: UUID, db: AsyncSession):
    user = await db.scalar(select(User).where(User.id == id))
    if not user:
        return ValueError("User not found with that id")
    return user



async def update_profile_service(id: UUID, to_update: user_schema.UpdateUser, db: AsyncSession):
    user = db.scalar(select(User).where(User.id == id, User.archived == False))
    if not user:
        raise ValueError("no value with that username")
    if to_update.email is not None:
        user.email = to_update.email
    if to_update.full_name is not None:
        user.full_name = to_update.full_name
    if to_update.phone is not None:
        user.phone = to_update.phone

    await db.commit()
    await db.refresh(user)
    return user
    
async def delete_user_service(id, db):
    user= db.scalar(select(User).where(User.id == id))
    if not user:
        raise ValueError("could not find user with that id")
    User.archived = True
    await db.commit()