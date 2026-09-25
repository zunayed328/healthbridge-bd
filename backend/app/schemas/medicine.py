from pydantic import BaseModel
from typing import Optional
import uuid


class MedicineCreate(BaseModel):
    brand_name: str
    generic_name: str
    manufacturer: Optional[str] = None
    strength: Optional[str] = None
    dosage_form: Optional[str] = None
    barcode: Optional[str] = None
    mrp: Optional[float] = None
    description: Optional[str] = None
    requires_prescription: bool = False


class MedicineResponse(BaseModel):
    id: uuid.UUID
    brand_name: str
    generic_name: str
    manufacturer: Optional[str] = None
    strength: Optional[str] = None
    dosage_form: Optional[str] = None
    barcode: Optional[str] = None
    mrp: Optional[float] = None
    requires_prescription: bool
    is_active: bool

    model_config = {"from_attributes": True}


class MedicineSearchResponse(BaseModel):
    total: int
    medicines: list[MedicineResponse]
