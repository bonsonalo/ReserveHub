from sqlalchemy import DATETIME, Integer, Boolean, String, ForeignKey, UUID, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from backend.app.core.database import Base
from typing import Any
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from .resource_availability import ResourceAvailability
from backend.app.model.resource_type import ResourceType
from .booking import Booking

class Resource(Base):
    __tablename__= "resources"

    id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        primary_key= True,
        default= uuid.uuid4
    )
    type_id: Mapped[uuid.UUID | None]= mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resource_types.id", ondelete="SET NULL")
    )
    code: Mapped[str]= mapped_column(
        String,
        unique=True
    )
    name: Mapped[str]= mapped_column(
        String
    )
    capacity: Mapped[int]= mapped_column(
        Integer,
        default= 1
    )
    location: Mapped[str]= mapped_column(
        String
    )
    attributes: Mapped[list[dict, Any]]= mapped_column(
        JSONB,
        server_default= text('{}::jsonb')
    )
    created_at: Mapped[datetime]= mapped_column(
        DATETIME,
        server_default= func.now()
    )
    updated_at: Mapped[datetime]= mapped_column(
        DATETIME,
        server_default= func.now(),
        onupdate= func.now()
    )
    resource_types: Mapped["ResourceType"]= relationship(
        back_populates= "resources"
    )
    resource_availabilty: Mapped[list[ResourceAvailability]]= relationship(
        cascade= "all, delete-orphan",
        back_populates= "resources"
    )
    bookings: Mapped[list["Booking"]]= relationship(
        back_populates= "resources",
        cascade= "save-update"
    )
    