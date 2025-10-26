from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from sqlalchemy import String, Integer, TIMESTAMP, UUID
from .associations import user_roles
from backend.app.core.database import Base
from backend.app.model.user import User

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
    users: Mapped["list[User]"]= relationship(
        secondary= user_roles,
        back_populates="roles"
    )