from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID, and_, exists, func, not_, select


from backend.app.model.booking import Booking
from backend.app.model.resource import Resource
from backend.app.model.resource_availability import ResourceAvailability
from backend.app.model.resource_type import ResourceType
from backend.app.core.logger import logger
from backend.app.schema import resource_schema
from backend.app.utils import resource_exist





async def get_all_resources_service(db: AsyncSession,
                                    sort_by: str,
                                    order: str,
                                    capacity: str | None,
                                    resource_type: str | None,
                                    available: bool= Query(False)                                    
                                    ):
    
    query= select(Resource)

    if capacity:
        query = query.where(Resource.capacity == capacity)

    if resource_type:
        type = await db.scalar(select(ResourceType).where(ResourceType.name == resource_type))
        if not type:
            logger.error("No resource type by that name")
            raise ValueError("No resource type by that error")
        query = query.where(Resource.type_id == type.id)
    if available:
        now = func.now()
        current_date= func.current_date()
        current_time= func.current_time()

        has_availability= exists().where(
            and_(
                ResourceAvailability.resource_id == Resource.id,
                ResourceAvailability.start_date <= current_date,
                ResourceAvailability.start_time <= current_time,
                ResourceAvailability.end_date >= current_date,
                ResourceAvailability.end_time >= current_time,
                ResourceAvailability.is_exception.is_(False)
            )
        )
        has_active_booking= exists().where(
            Booking.resource_id == Resource.id,
            Booking.status.notin_(["deleted", "cancelled"]),
            Booking.time_range.op("@>")(now)
        )

        query= query.where(
            and_(
                has_availability,
                not_(has_active_booking)
            )
        )
    if not hasattr(Resource, sort_by):
        logger.error(f"Invalid sort field: {sort_by}")
        raise AttributeError(f"Invalid sort field: {sort_by}")
    column_to_sort= getattr(Resource, sort_by)

    if order.lower() == "desc":
        query= query.order_by(column_to_sort.desc())
    if order.lower()== "asc":
        query= query.order_by(column_to_sort.asc())

    results= await db.scalars(query)
    final_resources= results.all()

    if not final_resources:
        logger.warning("No resource found for the given filter")
        return LookupError("no products found")
    logger.info(f"fetched {len(final_resources)} resources successfully")
    return final_resources




async def create_resource_service(info: resource_schema.CreateResource, db: AsyncSession):
    type_connect= await db.scalar(select(ResourceType).where(info.type_id == ResourceType.id))

    if not type_connect:
        return ValueError("Resource type does not exist")
    db_add= Resource(
        type_id= type_connect.id,
        code = info.code,
        name = info.name,
        capacity = info.capacity,
        location= info.location,
        attributes= info.attributes
    )
    db.add(db_add)
    await db.commit()
    await db.refresh(db_add)
    return db_add



async def get_resource_by_id_service(id: UUID, db: AsyncSession):
    resource= await db.scalar(select(Resource).where(Resource.id == id))
    resource_exist(resource)

    return resource




async def update_resource(id: UUID, updated_to: resource_schema.UpdateResource, db: AsyncSession):
    queried= await db.scalar(select(Resource).where(Resource.id == id))
    resource_exist(queried)
    if updated_to.type_id is not None:
        queried.type_id = updated_to.type_id
    if updated_to.code is not None:
        queried.code = updated_to.code
    if updated_to.name is not None:
        queried.name = updated_to.name
    if updated_to.capacity is not None:
        queried.capacity = updated_to.capacity


    await db.commit()
    await db.refresh(queried)
    return queried
    



async def delete_resource_service(id: UUID, db: AsyncSession):
    to_delete= await db.scalar(select(Resource).where(Resource.id == id))
    resource_exist(to_delete)
    await db.delete(to_delete)
    await db.commit()

