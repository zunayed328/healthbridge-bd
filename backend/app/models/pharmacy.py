import uuid
from sqlalchemy import String, Text, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


class Pharmacy(Base, TimestampMixin):
    __tablename__ = "pharmacies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    address: Mapped[str] = mapped_column(
        Text, nullable=True
    )
    area: Mapped[str] = mapped_column(
        String(100), nullable=True, index=True
    )
    city: Mapped[str] = mapped_column(
        String(100), default="Dhaka", nullable=False
    )
    phone: Mapped[str] = mapped_column(
        String(20), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    latitude: Mapped[float] = mapped_column(
        Numeric(10, 8), nullable=True
    )
    longitude: Mapped[float] = mapped_column(
        Numeric(11, 8), nullable=True
    )
    location: Mapped[str] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326),
        nullable=True,
    )

    inventory: Mapped[list["PharmacyInventory"]] = relationship(
        "PharmacyInventory",
        back_populates="pharmacy",
        lazy="select",
    )

    def __repr__(self):
        return f"<Pharmacy {self.name}>"
