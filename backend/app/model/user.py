from datetime import datetime
from backend.app.core.database import Base
import uuid
from sqlalchemy import UUID, String, Integer, Boolean, ForeignKey, TIMESTAMP, func
from typing import Optional

from backend.app.model.booking import Booking
from backend.app.model.booking_event import BookingEvent



from sqlalchemy.orm import Mapped, mapped_column, relationship






class User(Base):
    __tablename__= "users"

    id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default= uuid.uuid4
    )
    email: Mapped[str]= mapped_column(
        String,
        unique=True,
        nullable= False
    )
    hashed_password: Mapped[str]= mapped_column(
        String,
        nullable=False
    )
    full_name: Mapped[str]= mapped_column(
        String
    )
    phone: Mapped[str]= mapped_column(
        String
    )
    created_at: Mapped[datetime]= mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime]= mapped_column(
        TIMESTAMP(timezone=True),
        server_default= func.now(),
        onupdate= func.now()
    )
    archived: Mapped[bool]= mapped_column(
        Boolean,
        default= False
    )
    role: Mapped[str]= mapped_column(
        String,
        default= "user"
    )
    bookings: Mapped[list[Booking]]= relationship(
        back_populates= "users",
        cascade= "save-update"
    )
    booking_event: Mapped[list["BookingEvent"]]= relationship(
        back_populates= "user",
        cascade= "all, delete-orphan"
    )