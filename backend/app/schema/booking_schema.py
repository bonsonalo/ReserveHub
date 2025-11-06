from typing import Optional
from pydantic import BaseModel
from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import TSTZRANGE, JSONB


class CreateBooking(BaseModel):
    resource_id: UUID
    user_id: UUID
    status: Optional[str]
    time_range: TSTZRANGE
    attendees: Optional[int]
    data: Optional[JSONB]
    is_recurring: Optional[bool]
    recurrence_rule: str