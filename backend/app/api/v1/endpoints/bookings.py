from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from uuid import UUID

from backend.app.schema.booking_schema import CreateBooking
from backend.app.core.config import db_dependency, admin_dependency, user_dependency, superadmin_dependency
from backend.app.service.booking_service import create_booking_service, get_booking_by_id_service, get_booking_service
from backend.app.utils.authentication_check import authentication_check
from backend.app.core.logger import logger


router= APIRouter(
    prefix= "/api/v1/booking",
    tags= ["Bookings"]
)





# POST /api/v1/bookings	Customer/Staff/Admin	Create new booking. Supports Idempotency-Key to avoid duplicates.

@router.post("/create_booking", status_code=status.HTTP_201_CREATED)
async def create_booking(to_create: CreateBooking, current_user: admin_dependency, db: db_dependency):
    authentication_check(current_user)

    try:
        return await create_booking_service(to_create, db)
    except ValueError as e:
        logger.error(str(e))
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))


# GET /api/v1/bookings

@router.get("/get_all")
async def get_bookings(current_user: user_dependency, db: db_dependency, user_id: UUID= Query(None), resource_id: UUID= Query(None), booking_status: str= Query(None)):
    authentication_check(current_user)

    try:
        return await get_booking_service(current_user, db, user_id, resource_id, booking_status)
    except ValueError as e:
        logger.erro(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
    

# GET /api/v1/bookings/{id}   Authenticated   View booking details.

@router.get("/get_booking/{booking_id}")

async def get_booking_by_id(booking_id: UUID, current_user: user_dependency, db: db_dependency):
    authentication_check(current_user)
    try:
        return await get_booking_by_id_service(booking_id, current_user,  db)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
