from sqlalchemy import Integer, Boolean, String, ForeignKey, UUID, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from backend.app.core.database import Base
from typing import Any
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from datetime import datetime
from sqlalchemy import Enum as sqlEnum



from backend.app.schema.resource_schema import ResourceType
class Resource(Base):
    __tablename__= "resources"

    id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        primary_key= True,
        default= uuid.uuid4
    )
    code: Mapped[str]= mapped_column(
        String,
        unique=True
    )
    type: Mapped["ResourceType"]= mapped_column(
        sqlEnum(ResourceType, name= "resource_type", create_type= True),
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
    attributes: Mapped[dict[str, Any]]= mapped_column(
        JSONB,
        server_default= text("'{}'::jsonb")
    )
    created_at: Mapped[datetime]= mapped_column(
        TIMESTAMP,
        server_default= func.now()
    )
    updated_at: Mapped[datetime]= mapped_column(
        TIMESTAMP,
        server_default= func.now(),
        onupdate= func.now()
    )
    resource_availability: Mapped[list["ResourceAvailability"]]= relationship(
        cascade= "all, delete-orphan",
        back_populates= "resources"
    )
    bookings: Mapped[list["Booking"]]= relationship(
        back_populates= "resources",
        cascade= "save-update"
    )
    