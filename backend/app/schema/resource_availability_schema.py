from typing import Any, Optional
from pydantic import BaseModel
from datetime import time, date
from uuid import UUID

class AvailabilityTime(BaseModel):
    start_time: time
    end_time: time
    date: date

    class Config:
        from_attribute= True    # allows SQLAlchemy models to be converted automatically


class CreateResourceAvailability(BaseModel):
    recurrence: list[dict[str, Any]]
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    tz: Optional[str]= "UTC"
    is_exception: bool
    

class UpdatedTo(BaseModel):
    recurrence: Optional[list[dict[str, Any]]]= None
    start_date: Optional[date]= None
    end_date: Optional[date]= None
    start_time: Optional[time]= None
    end_time: Optional[time]= None
    tz: Optional[str]= "UTC"
    is_exception: Optional[bool]= None