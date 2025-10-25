from importlib.resources import Resource
from sqlalchemy import Integer, Boolean, String, TIMESTAMP, UUID, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import uuid
from backend.app.core.database import Base
from sqlalchemy.dialects.postgresql import JSONB
from typing import Any



class ResourceType(Base):
    __tablename__= "resource_types"


    id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        primary_key= True,
        server_default= uuid.uuid4
    )
    name: Mapped[str]= mapped_column(
        String,
        nullable= False
    )
    metadata: Mapped[dict[str, Any]]= mapped_column(
        JSONB,
        server_default= text('{}::jsonb')
    )
    resources: Mapped[list["Resource"]]= relationship(
        back_populates= "resource_types",
        cascade="save-update"
    )