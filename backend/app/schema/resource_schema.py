from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import JSONB



class CreateResource(BaseModel):
    type_id: UUID
    code: str
    name: str
    capacity: Optional[int]
    location: str
    attributes: JSONB



class UpdateResource(BaseModel):
    type_id: Optional[id]
    code: Optional[str]
    name: Optional[str]
    capacity: Optional[int]
    location: Optional[str]
    attributes: Optional[JSONB]
    