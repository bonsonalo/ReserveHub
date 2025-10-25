from datetime import datetime
from backend.app.core.database import Base
import uuid
from sqlalchemy import UUID, String, Integer, Boolean, ForeignKey, TIMESTAMP, func
from typing import Optional


from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.role import Role




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
    password_hash: Mapped[str]= mapped_column(
        String,
        nullable=False
    )
    full_name: Mapped[str]= mapped_column(
        String
    )
    phone: Mapped[str]= mapped_column(
        String
    )
    role_id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE")
    )
    roles: Mapped["Role"]= relationship(
        back_populates= "users"
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