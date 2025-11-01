from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import UUID
import uuid




class UpdateUser(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    phone: Optional[str]

