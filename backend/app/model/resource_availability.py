from sqlalchemy import String, Boolean, UUID, func, ForeignKey, text, TIMESTAMP, DATE, TIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any
import uuid
from sqlalchemy.dialects.postgresql import JSONB
from backend.app.core.database import Base
from datetime import datetime, time, date

class ResourceAvailability(Base):
    __tablename__= "resource_availability"



    id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid= True),
        primary_key= True,
        default= uuid.uuid4
    )
    resource_id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid= True),
        ForeignKey("resources.id", ondelete="CASCADE")
    )
    recurrence: Mapped[list[dict[str, Any]]]= mapped_column(
        JSONB,
        default= text('{}::jsonb')
    )
    start_date: Mapped[DATE] = mapped_column(
        DATE,
        nullable=False
    )
    end_date: Mapped[date] = mapped_column(
        DATE,
        nullable=False
    )
    start_time: Mapped[time]= mapped_column(
        TIME,
        nullable= False
    )
    end_time: Mapped[time]= mapped_column(
        TIME,
        nullable= False
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
        back_populates= "resource_availability"
    )