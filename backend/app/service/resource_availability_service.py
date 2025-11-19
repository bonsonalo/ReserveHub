from sqlalchemy import and_, exists, not_, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional
from uuid import UUID

from backend.app.model.booking import Booking
from backend.app.model.resource import Resource
from backend.app.model.resource_availability import ResourceAvailability
from backend.app.schema.resource_availability_schema import CreateResourceAvailability, UpdateAvailabilityRequest
from backend.app.utils.resource_exist import resource_exist
from backend.app.core.logger import logger
from backend.app.utils.scheduling import has_conflict



async def get_resource_availabilty_by_id_service(resource_id: UUID, db: AsyncSession, date: Optional[date]= None):

    resource= await db.scalar(select(Resource).where(Resource.id == resource_id))
    resource_exist(resource)
    now = func.now()

    query = select(ResourceAvailability.start_time, ResourceAvailability.end_time).where(ResourceAvailability.resource_id == resource_id)

    if date:
        query= query.where(
            ResourceAvailability.start_date <= date,
            ResourceAvailability.end_date >= date
        )

    has_active_booking= exists().where(
            Booking.resource_id == Resource.id,
            Booking.status.notin_(["deleted", "cancelled", "booked"]),
            Booking.time_range.op("@>")(now)
        )
    
    query= query.where(not_(has_active_booking))

    result= await db.execute(query)
    availabilties= result.all()

    if not availabilties:
        logger.warning("No availabilites")
        return {"No Availabilites found"}
    return [
        {"start_time": start, "end_point": end} for start, end in availabilties
    ]
    

async def create_resource_availability_service(resource_id: UUID, info: CreateResourceAvailability, db: AsyncSession):
    db_add= ResourceAvailability(
        resource_id= resource_id,
        recurrence= info.recurrence,
        start_date= info.start_date,
        end_date= info.end_date,
        start_time= info.start_time,
        end_time= info.end_time,
        tz= info.tz,
        is_exception= info.is_exception
    )

    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add


async def patch_resource_availability_by_id_service(id: UUID, updated_data: UpdateAvailabilityRequest, db: AsyncSession):
    #fetch availability
    availability= await db.scalar(select(ResourceAvailability).where(ResourceAvailability.id == id))
    resource_exist(availability)
    

    #list all existint resource availabilies of the same resource excluding the one we are updating
    existing_availabilities= await db.scalars(select(ResourceAvailability).where(
        ResourceAvailability.resource_id == availability.resource_id,
        ResourceAvailability.id != availability.id
    )).all()

    # load the existing bookings for that particular resource

    existing_booking= await db.scalar(select(Booking).where(Booking.resource_id == availability.resource_id)).all()


    if has_conflict(updated_data, existing_availabilities, existing_booking):
        raise FileExistsError
    
    if updated_data.start_date is not None:
        availability.start_date = updated_data.start_date
    if updated_data.end_date is not None:
        availability.end_date = updated_data.end_date
    if updated_data.start_time is not None:
        availability.start_time = updated_data.start_time
    if updated_data.end_time is not None:
        availability.end_time = updated_data.end_time
    if updated_data.tz is not None:
        availability.tz = updated_data.tz
    if updated_data.is_exception is not None:
        availability.is_exception = updated_data.is_exception

    await db.commit()
    await db.refresh(availability)

    return availability



