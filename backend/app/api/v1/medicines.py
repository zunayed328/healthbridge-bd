import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from app.core.database import get_db
from app.models.medicine import MedicineCatalog
from app.schemas.medicine import (
    MedicineCreate,
    MedicineResponse,
    MedicineSearchResponse,
)

router = APIRouter(prefix="/medicines", tags=["Medicines"])


@router.get("/search", response_model=MedicineSearchResponse)
async def search_medicines(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    search = f"%{q}%"
    query = select(MedicineCatalog).where(
        MedicineCatalog.is_active == True,
        or_(
            MedicineCatalog.brand_name.ilike(search),
            MedicineCatalog.generic_name.ilike(search),
            MedicineCatalog.manufacturer.ilike(search),
        ),
    )
    count_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = count_result.scalar()

    result = await db.execute(query.offset(offset).limit(limit))
    medicines = result.scalars().all()

    return MedicineSearchResponse(total=total, medicines=medicines)


@router.get("/{medicine_id}", response_model=MedicineResponse)
async def get_medicine(
    medicine_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MedicineCatalog).where(
            MedicineCatalog.id == medicine_id,
            MedicineCatalog.is_active == True,
        )
    )
    medicine = result.scalar_one_or_none()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


@router.get("/barcode/{barcode}", response_model=MedicineResponse)
async def get_medicine_by_barcode(
    barcode: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MedicineCatalog).where(
            MedicineCatalog.barcode == barcode,
            MedicineCatalog.is_active == True,
        )
    )
    medicine = result.scalar_one_or_none()
    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found in catalog",
        )
    return medicine


@router.post("/", response_model=MedicineResponse, status_code=201)
async def create_medicine(
    medicine_data: MedicineCreate,
    db: AsyncSession = Depends(get_db),
):
    medicine = MedicineCatalog(
        id=uuid.uuid4(),
        **medicine_data.model_dump(),
        is_active=True,
    )
    db.add(medicine)
    await db.commit()
    await db.refresh(medicine)
    return medicine
