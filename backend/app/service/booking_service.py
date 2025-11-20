from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.model.booking import Booking
from backend.app.schema.booking_schema import CreateBooking




async def create_booking_service(to_create: CreateBooking, db: AsyncSession):
    db_add= Booking(
        resource_id= to_create.resource_id,
        user_id= to_create.user_id,
        status= to_create.user_id,
        time_range= to_create.time_range,
        attendees= to_create.attendees,
        data= to_create.data,
        is_recurring= to_create.is_recurring,
        recurrence_rule= to_create.recurrence_rule
    )

    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)

    return db_add