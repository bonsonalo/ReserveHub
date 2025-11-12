from pydantic import BaseModel, EmailStr





class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: str


class Token(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str