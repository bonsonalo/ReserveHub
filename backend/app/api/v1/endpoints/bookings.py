from fastapi import APIRouter, Depends, HTTPException
from starlette import status


from backend.app.schema.booking_schema import CreateBooking
from backend.app.core.config import db_dependency, admin_dependency, user_dependency, superadmin_dependency
from backend.app.service.booking_service import create_booking_service
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
