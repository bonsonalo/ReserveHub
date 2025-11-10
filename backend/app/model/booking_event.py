from __future__ import annotations
from sqlalchemy import String, Integer, Boolean, func, ForeignKey, UUID, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any
import uuid
from backend.app.core.database import Base

from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from datetime import datetime



class BookingEvent(Base):
    __tablename__= "booking_events"


    id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid= True),
        primary_key= True,
        default= uuid.uuid4
    )
    booking_id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid= True),
        ForeignKey("bookings.id", ondelete= "CASCADE"),
        default= uuid.uuid4
    )
    event_type: Mapped[str]= mapped_column(
        String
    )
    payload: Mapped[dict[str, Any]]=  mapped_column(
        JSONB,
        server_default= text("'{}'::jsonb")
    )
    actor_id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid= True),
        ForeignKey("users.id", ondelete= "CASCADE"),
        default= uuid.uuid4
    )
    occurred_at: Mapped[datetime]= mapped_column(
        TIMESTAMP(timezone=True),
        server_default= func.now()
    )

    user: Mapped["User"]= relationship(
        back_populates= "booking_event"
    )
    booking: Mapped["Booking"]= relationship(
        back_populates= "booking_event"
    )