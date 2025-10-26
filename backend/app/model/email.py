from sqlalchemy import Integer, String, Boolean, func, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from datetime import datetime
from backend.app.core.database import Base
from backend.app.model.booking import Booking
from sqlalchemy.dialects.postgresql import TIMESTAMP

class Email(Base):
    __tablename__= "emails"



    id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        primary_key= True,
        server_default= uuid.uuid4
    )
    booking_id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid= True),
        ForeignKey("bookings.id", ondelete= "CASCADE"),
        server_default= uuid.uuid4
    )
    to_email: Mapped[str]= mapped_column(
        String
    )
    subject: Mapped[str]= mapped_column(
        String
    )
    body: Mapped[str]= mapped_column(
        String
    )
    status: Mapped[str]= mapped_column(
        String,
        default= "pending"
    )
    attempt: Mapped[int]=mapped_column(
        Integer,
        default= 0
    )
    next_try: Mapped[datetime]= mapped_column(
        TIMESTAMP(timezone= True)
    )
    created_at: Mapped[datetime]= mapped_column(
        TIMESTAMP(timezone= True),
        server_default= func.now()
    )




    bookings: Mapped["Booking"]=relationship(
        back_populates= "emails"
    )