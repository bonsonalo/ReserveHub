from typing import Optional, Any
from pydantic import BaseModel, Json
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum



class ResourceType(str, Enum):
    room= "room"
    conference= "conference"
    library= "library"
    

class ReturnResourceById(BaseModel):
    type: ResourceType
    code: str
    name: str
    capacity: Optional[int]
    location: str
    attributes: Optional[dict[str, Any]]

class CreateResource(BaseModel):
    type: ResourceType
    code: str
    name: str
    capacity: Optional[int]
    location: str
    attributes: Optional[dict[str, Any]]



class UpdateResource(BaseModel):
    type: Optional[ResourceType]
    code: Optional[str]
    name: Optional[str]
    capacity: Optional[int]
    location: Optional[str]
    attributes: Optional[dict[str, Any]]
    