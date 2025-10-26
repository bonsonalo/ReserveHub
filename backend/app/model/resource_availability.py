from .resource import Resource
from sqlalchemy import Integer, String, Boolean, UUID, func, ForeignKey, text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any
import uuid
from sqlalchemy.dialects.postgresql import JSONB
from backend.app.core.database import Base
from datetime import datetime

class ResourceAvailability(Base):
    __tablename__= "resource_availability"



    id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid= True),
        primary_key= True,
        server_default= uuid.uuid4
    )
    resource_id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid= True),
        ForeignKey("resources.id", ondelete="CASCADE")
    )
    recurrence: Mapped[list[dict, Any]]= mapped_column(
        JSONB,
        server_default= text('{}::jsonb')
    )
    start_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False
    )
    end_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False
    )
    tz: Mapped[str]= mapped_column(
        String,
        nullable= False,
        server_default="UTC"
    )
    is_exception: Mapped[bool]= mapped_column(
        Boolean,
        default=False
    )

    resources: Mapped["Resource"]= relationship(
        back_populates= "resource_availabilty"
    )