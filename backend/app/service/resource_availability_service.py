from sqlalchemy import UUID, and_, exists, not_, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional


from backend.app.model.booking import Booking
from backend.app.model.resource import Resource
from backend.app.model.resource_availability import ResourceAvailability
from backend.app.utils import resource_exist
from backend.app.core.logger import logger



async def get_resource_availabilty_by_id_service(resource_id: UUID, date: Optional[date], db: AsyncSession):

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
    