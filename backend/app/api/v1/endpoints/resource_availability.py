from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from datetime import date
from starlette import status 

from backend.app.core.config import user_dependency, admin_dependency, superadmin_dependency, db_dependency
from backend.app.schema.resource_availability_schema import CreateResourceAvailability, UpdateAvailabilityRequest
from backend.app.service.resource_availability_service import create_resource_availability_service, delete_resource_availability_by_id_service, get_resource_availabilty_by_id_service, patch_resource_availability_by_id_service
from backend.app.core.logger import logger
from backend.app.utils.authentication_check import authentication_check

router= APIRouter(
    prefix= "/api/v1",
    tags= ["resource_availabilty"]
)




# GET /api/v1/resources/{id}/availability
@router.get("/resource/{resource_id}/resource_availabilty")
async def get_resource_availabilty_by_id(resource_id: UUID, current_user: user_dependency, db: db_dependency, date: Optional[date]= Query(None)):
    authentication_check(current_user)
    try:
        return await get_resource_availabilty_by_id_service(resource_id, db, date)
    except ValueError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
            
# POST /api/v1/resources/{id}/availability

@router.post("/resource/{resource_id}/availability", status_code=status.HTTP_201_CREATED)
async def create_resource_availability(resource_id: UUID, info: CreateResourceAvailability, current_user: admin_dependency, db: db_dependency):
    authentication_check(admin_dependency)

    try:
        return await create_resource_availability_service(resource_id, info, db)
    except ValueError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
    

# PATCH /api/v1/resource-availabilities/{id}

@router.patch("/resource-availabilities/{id}")
async def patch_resource_availability_by_id(id: UUID, updated_to: UpdateAvailabilityRequest, current_user: superadmin_dependency, db: db_dependency):
    authentication_check(current_user)

    try:
        return await patch_resource_availability_by_id_service(id, updated_to, db)
    except FileExistsError as e:
        logger.error("there is time overlap")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= str(e))
    
# DELETE /api/v1/resource-availabilities/{id}

@router.delete("/resource_availabilities/{id}")
async def delete_resource_availability_by_id(id: UUID, db:db_dependency, current_user: superadmin_dependency):
    authentication_check(current_user)

    try:
        return await delete_resource_availability_by_id_service(id, db)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))

