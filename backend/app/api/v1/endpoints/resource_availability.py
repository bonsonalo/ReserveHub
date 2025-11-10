from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from datetime import date
from starlette import status 

from backend.app.core.config import user_dependency, admin_dependency, superadmin_dependency, db_dependency
from backend.app.service.auth_service import authenticate_user
from backend.app.service.resource_availability_service import get_resource_availabilty_by_id_service
from backend.app.core.logger import logger

router= APIRouter(
    prefix= "/api/v1",
    tags= ["resource_availabilty"]
)




# GET /api/v1/resources/{id}/availability
@router.get("/resource/{resource_id}/resource_availabilty")
async def get_resource_availabilty_by_id(resource_id: UUID, date: Optional[date], current_user: user_dependency, db: db_dependency):
    authenticate_user(current_user)
    try:
        return await get_resource_availabilty_by_id_service(resource_id, date, db)
    except ValueError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
            

