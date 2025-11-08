from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from sqlalchemy.dialects.postgresql import UUID
from starlette import status

from backend.app.model.resource import Resource
from backend.app.core.config import user_dependency, admin_dependency, superadmin_dependency, db_dependency
from backend.app.service.auth_service import authenticate_user
from backend.app.service.resource_service import create_resource_service, delete_resource_service, get_all_resources_service, get_resource_by_id_service
from backend.app.core.logger import logger
from backend.app.schema import resource_schema







router= APIRouter(
    prefix= "/api/v1/resource",
    tags= ["resource"]
)


# create resource
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_resource(info: resource_schema.Resource, current_user: admin_dependency, db: db_dependency):
    authenticate_user(current_user)
    try:
        return await create_resource_service(info, db)
    except ValueError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
    

# filter by type, capacity, availablity
@router.get("/get_all", status.HTTP_200_OK)
async def get_all_resources(db: db_dependency,
                            current_user: user_dependency,
                            sort_by: str= Query("id"),
                            order: str= Query("asc"),
                            capacity: Optional[str]= Query(None),
                            resource_type: Optional[resource_schema.ResourceType]= Query(None),
                            available: Optional[bool]= Query(False)                           
                            ):
    authenticate_user(current_user)
    try:
        return await get_all_resources_service(db,
                                               sort_by,
                                               order,
                                               capacity,
                                               resource_type,
                                               available)
    
    except ValueError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(e))
    except LookupError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
    except AttributeError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(e))
    



# get resource by id
@router.get("/get/{id}", status_code=status.HTTP_200_OK)
async def get_resource_by_id(id: UUID, current_user: user_dependency, db: db_dependency):
    authenticate_user(current_user)
    try:
        return await get_resource_by_id_service(id, db)
    except ValueError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
    


# update resource
@router.patch("/update/{id}")
async def update_resource(id: UUID, updated_to: resource_schema.UpdateResource, current_user: admin_dependency, db: db_dependency):
    authenticate_user(current_user)
    try:
        return await update_resource(id,updated_to, db)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
    

# DELETE /api/v1/resources/{id}
@router.delete("/delete/{id}")
async def delete_resource(id: UUID, current_user: superadmin_dependency, db: db_dependency):
    authenticate_user(current_user)
    try:
        return await delete_resource_service(id,db)

    except Exception as e:
        logger.error(str(e))
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
