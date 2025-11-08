from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum



class ResourceType(str, Enum):
    room= "room"
    conference= "conference"
    dinning_hall= "library"
    
class CreateResource(BaseModel):
    type: ResourceType
    code: str
    name: str
    capacity: Optional[int]
    location: str
    attributes: JSONB



class UpdateResource(BaseModel):
    type: Optional[ResourceType]
    code: Optional[str]
    name: Optional[str]
    capacity: Optional[int]
    location: Optional[str]
    attributes: Optional[JSONB]
    