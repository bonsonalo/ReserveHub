from pydantic import BaseModel
from datetime import time, date



class AvailabilityTime(BaseModel):
    start_time: time
    end_time: time
    date: date

    class Config:
        from_attribute= True    # allows SQLAlchemy models to be converted automatically