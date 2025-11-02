from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from sqlalchemy.dialects.postgresql import UUID
from starlette import status

from backend.app.model.resource import Resource
from backend.app.core.config import user_dependency, admin_dependency, superadmin_dependency, db_dependency
from backend.app.service.auth_service import authenticate_user
from backend.app.service.resource_service import get_all_resources_service
from backend.app.core.logger import logger








router= APIRouter(
    prefix= "/api/v1/resource",
    tags= ["resource"]
)



# filter by type, capacity, availablity
@router.get("/get_all", status.HTTP_200_OK)
async def get_all_resources(db: db_dependency,
                            current_user: user_dependency,
                            sort_by: str= Query("id"),
                            order: str= Query("asc"),
                            capacity: Optional[str]= Query(None),
                            resource_type: Optional[str]= Query(None),
                            available: Optional[str]= Query(None)                           
                            ):
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
