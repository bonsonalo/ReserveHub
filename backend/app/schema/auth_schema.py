from pydantic import BaseModel



class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str