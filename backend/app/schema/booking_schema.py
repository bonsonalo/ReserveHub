from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Enum as sqlEnum
from sqlalchemy.dialects.postgresql import TSTZRANGE, JSONB
from enum import Enum
from uuid import UUID

class BookingStatus(str, sqlEnum):
    booked= "booked"
    cancelled= "cancelled"
    deleted= "deleted"



class CreateBooking(BaseModel):
    resource_id: UUID
    user_id: UUID
    status: Optional[str]= None
    time_range: TSTZRANGE
    attendees: Optional[int]= None
    data: Optional[dict]= None
    is_recurring: Optional[bool]= None
    recurrence_rule: str


class UpdateRequest(BaseModel):
    status: Optional[str]= None
    attendees: Optional[int]= None
    data: Optional[JSONB]= None