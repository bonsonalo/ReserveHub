from fastapi import APIRouter


from backend.app.api.v1.endpoints.auth import router as auth_router
from backend.app.api.v1.endpoints.resource import router as resource_router
from backend.app.api.v1.endpoints.resource_availability import router as availability_router
from backend.app.api.v1.endpoints.user import router as user_router





routers = APIRouter()
router_list= [auth_router, resource_router, availability_router, user_router]

for router in router_list:
    routers.include_router(router)