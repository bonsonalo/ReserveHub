from sqlalchemy import Boolean, Integer, ForeignKey, String, func, UUID, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from backend.app.core.database import Base
from sqlalchemy.dialects.postgresql import TSTZRANGE, JSONB, TIMESTAMP, Range
from datetime import datetime
from typing import Any




class Booking(Base):
    __tablename__= "bookings"

    id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid= True),
        primary_key=True,
        default= uuid.uuid4
    )
    resource_id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resources.id", ondelete="SET NULL"),
        nullable= True
    )
    user_id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete= "SET NULL")
    )
    status: Mapped[str]= mapped_column(
        String,
        nullable= False,
        default= "pending",
        server_default= text("'pending'")
    )
    time_range: Mapped[Range[datetime]]= mapped_column(
        TSTZRANGE,
        nullable= False
    )
    attendees: Mapped[int] = mapped_column(
        Integer,
        default= 1
    )
    data: Mapped[dict[str, Any]]= mapped_column(
        JSONB,
        server_default= text("'{}'::jsonb")   
    )
    created_by: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid= True),
        ForeignKey("users.id", ondelete= "SET NULL")
    )
    created_at: Mapped[datetime]= mapped_column(
        TIMESTAMP(timezone= True),
        server_default= func.now()
    )
    updated_at: Mapped[datetime]= mapped_column(
        TIMESTAMP(timezone= True),
        server_default= func.now(),
        onupdate= func.now()
    )
    canceled_at: Mapped[datetime]= mapped_column(
        TIMESTAMP(timezone= True),
        nullable= True
    )
    is_recurring: Mapped[bool]= mapped_column(
        Boolean,
        default= False
    )
    recurrence_rule: Mapped[str]= mapped_column(
        String
    )




    resources: Mapped["Resource | None"]= relationship(
        back_populates= "bookings"
    )
    user: Mapped["User | None"]= relationship(
        back_populates= "bookings",
        foreign_keys= "[Booking.user_id]"
    )
    creator: Mapped["User | None"]= relationship(
        back_populates= "created_bookings",
        foreign_keys= "[Booking.created_by]"
    )
    booking_event: Mapped[list["BookingEvent"]]= relationship(
        back_populates= "booking",
        cascade= "all, delete-orphan"
    )
    emails: Mapped[list["Email"]]= relationship(
        back_populates= "bookings",
        cascade= "all, delete-orphan"
    )