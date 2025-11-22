from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
from sqlalchemy.dialects.postgresql import TSTZRANGE


from backend.app.model.booking import Booking
from backend.app.schema.booking_schema import CreateBooking, UpdateRequest
from backend.app.utils.resource_exist import resource_exist



async def create_booking_service(to_create: CreateBooking, db: AsyncSession):

    time_range= func.tstzrange(
        to_create.start_time,
        to_create.end_time
    )
    db_add= Booking(
        resource_id= to_create.resource_id,
        user_id= to_create.user_id,
        status= to_create.status,
        time_range= time_range,
        attendees= to_create.attendees,
        data= to_create.data,
        is_recurring= to_create.is_recurring,
        recurrence_rule= to_create.recurrence_rule,
        created_by= to_create.created_by
    )

    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)

    return db_add



async def get_booking_service(current_user, db: AsyncSession, user_id: UUID | None, resource_id: UUID | None, booking_status: str):

    current_id= current_user["id"]
    current_role= current_user["role"]
    query= select(Booking)

    if current_role not in ["admin", "superadmin"]:
        query = query.where(Booking.user_id == current_id)
    if user_id:
        query = query.where(Booking.user_id == user_id)
    if resource_id:
        query = query.where(Booking.resource_id == resource_id)
    if booking_status:
        query= query.where(Booking.status == booking_status)

    result= await db.scalars(query)
    return result.all()

async def get_booking_by_id_service(booking_id: UUID, current_user, db: AsyncSession):
    current_role= current_user["role"]
    current_id= current_user["id"]

    query= select(Booking)

    if current_role not in ["admin", "superadmin"]:
        query= query.where((Booking.user_id == current_id) & (Booking.id == booking_id))
    else:
        query = query.where(Booking.id == booking_id)

    result = await db.scalars(query)
    return result.all()



async def update_booking_service(booking_id: UUID, to_update: UpdateRequest, db: AsyncSession):
    query= await db.scalar(select(Booking).where(Booking.id== booking_id))
    resource_exist(query)

    if to_update.attendees is not None:
        query.attendees = to_update.attendees
    if to_update.status is not None:
        query.status = to_update.status
    if to_update.data is not None:
        query.data = to_update

    await db.commit()
    await db.refresh(query)

    return query