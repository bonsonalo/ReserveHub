from fastapi import APIRouter, HTTPException
from starlette import status
from uuid import UUID



from backend.app.core.config import user_dependency, admin_dependency, superadmin_dependency, db_dependency
from backend.app.service.user_service import delete_user_service, get_user_by_id_service, get_user_info_service, get_users_service, update_profile_service, update_user_service
from backend.app.core.logger import logger
from backend.app.utils.authentication_check import authentication_check
from backend.app.schema import user_schema

router= APIRouter(
    prefix= "/api/v1/users",
    tags= ["users"]
)



@router.get("/get_all", response_model= list[user_schema.UserResponse], status_code= status.HTTP_200_OK)
async def get_users(current_user: admin_dependency, db: db_dependency):
    authentication_check(current_user)
    try:
        return await get_users_service(db)
    except ValueError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(e))
    except LookupError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
    


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_info(current_user: user_dependency, db: db_dependency):
    authentication_check(current_user)

    try:
        return await get_user_info_service(current_user["id"], db)
    except ValueError:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "user not found")

@router.patch("/update", status_code=status.HTTP_200_OK)
async def update_user(id: UUID, user: user_schema.UpdateUser, current_user: superadmin_dependency, db: db_dependency):
    authentication_check(current_user)
    try:
        return await update_user_service(id, user, db)
    except LookupError as e:
        logger.error(str(e))
        HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= str(e))
    except Exception as e:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))


@router.get("/get/{id}", status_code= status.HTTP_200_OK)
async def get_user_by_id(id: UUID, current_user: admin_dependency, db: db_dependency):
    authentication_check(current_user)
    try:
        return await get_user_by_id_service(id, db)
    except ValueError as e:
        logger.error(str(e))
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))

# update user info for your profile

@router.patch("/update_profile", status_code=status.HTTP_200_OK)
async def update_profile(user: user_schema.UpdateUser, db: db_dependency, current_user: user_dependency):
    authentication_check(current_user)
    try:
        return await update_profile_service(current_user["id"], user, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
    

# soft-delete user


@router.delete("/delete/{id}")
async def delete_user(id: UUID, current_user: superadmin_dependency, db: db_dependency):
    authentication_check(current_user)
    try:
        return await delete_user_service(id, db)
    except ValueError as e:
        logger.error(str(e))
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))



