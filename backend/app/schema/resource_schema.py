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
    capacity: Optional[int]= None
    location: str
    attributes: Optional[dict[str, Any]]= None

    model_config= {
        'from_attributes': True
    }

class CreateResource(BaseModel):
    type: ResourceType
    code: str
    name: str
    capacity: Optional[int]= None
    location: str
    attributes: Optional[dict[str, Any]]= None



class UpdateResource(BaseModel):
    type: Optional[ResourceType]= None
    code: Optional[str]= None
    name: Optional[str]= None
    capacity: Optional[int]= None
    location: Optional[str]= None
    attributes: Optional[dict[str, Any]]= None
    