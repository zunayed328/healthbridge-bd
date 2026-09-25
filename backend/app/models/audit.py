import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin


class AuditEvent(Base, TimestampMixin):
    __tablename__ = "audit_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    actor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    action: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )
    resource_type: Mapped[str] = mapped_column(
        String(100), nullable=True
    )
    resource_id: Mapped[str] = mapped_column(
        String(255), nullable=True
    )
    details: Mapped[dict] = mapped_column(
        JSONB, nullable=True
    )
    ip_address: Mapped[str] = mapped_column(
        String(45), nullable=True
    )

    def __repr__(self):
        return f"<AuditEvent {self.action}>"
