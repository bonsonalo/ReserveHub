
from sqlalchemy import Column, Table, UUID, ForeignKey
from backend.app.core.database import Base





user_roles= Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        Column(
            "role_id",
            UUID(as_uuid=True),
            ForeignKey("roles.id", ondelete="CASCADE")
        )
    )
)