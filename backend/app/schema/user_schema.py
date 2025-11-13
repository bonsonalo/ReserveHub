from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import UUID
import uuid
from datetime import date



class UpdateUser(BaseModel):
    email: Optional[EmailStr]= None
    full_name: Optional[str]= None
    phone: Optional[str]= None


class UserResponse(BaseModel):
    email: EmailStr
    full_name: str
    phone: str
    created_at: date
    updated_at: date
    archived: bool
    role: str

