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
    