from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Enum as sqlEnum
from sqlalchemy.dialects.postgresql import TSTZRANGE, JSONB
from enum import Enum
from uuid import UUID
from datetime import datetime
class BookingStatus(str, sqlEnum):
    booked= "booked"
    cancelled= "cancelled"
    deleted= "deleted"

class CreateBooking(BaseModel):
    resource_id: UUID
    user_id: UUID
    status: Optional[str]= None
    start_time: datetime
    end_time: datetime
    attendees: Optional[int]= Field(None, ge= 1)
    data: Optional[dict]= None
    is_recurring: Optional[bool]= None
    recurrence_rule: Optional[str]= None
    created_by: UUID


class UpdateRequest(BaseModel):
    status: Optional[str]= None
    attendees: Optional[int]= None
    data: Optional[dict]= None

class RescheduleBooking(BaseModel):
    start_time: datetime
    end_time: datetime