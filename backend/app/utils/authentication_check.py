from fastapi import HTTPException
from starlette import status

def authentication_check(value):
    if not value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "user not validated")