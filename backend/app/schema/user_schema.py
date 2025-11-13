from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import UUID
import uuid
from datetime import date



class UpdateUser(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    phone: Optional[str]


class UserResponse(BaseModel):
    email: EmailStr
    full_name: str
    phone: str
    created_at: date
    updated_at: date
    archived: bool
    role: str
    
