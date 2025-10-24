from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy import String, Integer, TIMESTAMP, UUID

from backend.app.core.database import Base

class Role(Base):
    __tablename__= "roles"


    id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid= True),
        primary_key=True,
        default= uuid.uuid4
    )
    name: Mapped[str]= mapped_column(
        unique= True,
        nullable=False
    )