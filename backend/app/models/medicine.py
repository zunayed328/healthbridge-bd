import uuid
from sqlalchemy import String, Text, Boolean, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


class MedicineCatalog(Base, TimestampMixin):
    __tablename__ = "medicine_catalog"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    brand_name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    generic_name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    manufacturer: Mapped[str] = mapped_column(
        String(255), nullable=True
    )
    strength: Mapped[str] = mapped_column(
        String(100), nullable=True
    )
    dosage_form: Mapped[str] = mapped_column(
        String(100), nullable=True
    )
    barcode: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=True, index=True
    )
    mrp: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    requires_prescription: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    extra_data: Mapped[dict] = mapped_column(
        JSONB, nullable=True
    )

    inventory_items: Mapped[list["PharmacyInventory"]] = relationship(
        back_populates="medicine",
        lazy="select",
    )

    def __repr__(self):
        return f"<Medicine {self.brand_name} {self.strength}>"


class PharmacyInventory(Base, TimestampMixin):
    __tablename__ = "pharmacy_inventory"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    pharmacy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    medicine_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("medicine_catalog.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    stock_status: Mapped[str] = mapped_column(
        String(20), default="unknown", nullable=False
    )
    quantity: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    price: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    is_available: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    medicine: Mapped["MedicineCatalog"] = relationship(
        back_populates="inventory_items"
    )
    pharmacy: Mapped["Pharmacy"] = relationship(
        back_populates="inventory"
    )

    def __repr__(self):
        return f"<Inventory {self.medicine_id} @ {self.pharmacy_id}>"
