import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.medicine import MedicineCatalog

SAMPLE_MEDICINES = [
    {
        "brand_name": "Napa",
        "generic_name": "Paracetamol",
        "manufacturer": "Beximco Pharmaceuticals",
        "strength": "500mg",
        "dosage_form": "Tablet",
        "barcode": "8901234567890",
        "mrp": 1.50,
        "description": "Pain reliever and fever reducer",
        "requires_prescription": False,
    },
    {
        "brand_name": "Napa Extra",
        "generic_name": "Paracetamol + Caffeine",
        "manufacturer": "Beximco Pharmaceuticals",
        "strength": "500mg + 65mg",
        "dosage_form": "Tablet",
        "barcode": "8901234567891",
        "mrp": 2.00,
        "description": "Extra strength pain reliever",
        "requires_prescription": False,
    },
    {
        "brand_name": "Ace",
        "generic_name": "Paracetamol",
        "manufacturer": "Square Pharmaceuticals",
        "strength": "500mg",
        "dosage_form": "Tablet",
        "barcode": "8901234567892",
        "mrp": 1.50,
        "description": "Pain reliever and fever reducer",
        "requires_prescription": False,
    },
    {
        "brand_name": "Histacin",
        "generic_name": "Chlorpheniramine",
        "manufacturer": "Square Pharmaceuticals",
        "strength": "4mg",
        "dosage_form": "Tablet",
        "barcode": "8901234567893",
        "mrp": 3.00,
        "description": "Antihistamine for allergy relief",
        "requires_prescription": False,
    },
    {
        "brand_name": "Seclo",
        "generic_name": "Omeprazole",
        "manufacturer": "Square Pharmaceuticals",
        "strength": "20mg",
        "dosage_form": "Capsule",
        "barcode": "8901234567894",
        "mrp": 5.00,
        "description": "Proton pump inhibitor for acidity",
        "requires_prescription": True,
    },
    {
        "brand_name": "Amoxil",
        "generic_name": "Amoxicillin",
        "manufacturer": "GlaxoSmithKline",
        "strength": "500mg",
        "dosage_form": "Capsule",
        "barcode": "8901234567895",
        "mrp": 8.00,
        "description": "Antibiotic for bacterial infections",
        "requires_prescription": True,
    },
    {
        "brand_name": "ORS",
        "generic_name": "Oral Rehydration Salts",
        "manufacturer": "ACME Laboratories",
        "strength": "27.9g",
        "dosage_form": "Powder",
        "barcode": "8901234567896",
        "mrp": 15.00,
        "description": "Oral rehydration solution for diarrhea",
        "requires_prescription": False,
    },
    {
        "brand_name": "Insulin Mixtard",
        "generic_name": "Insulin (Human)",
        "manufacturer": "Novo Nordisk",
        "strength": "30/70 IU/ml",
        "dosage_form": "Injection",
        "barcode": "8901234567897",
        "mrp": 450.00,
        "description": "Insulin for diabetes management",
        "requires_prescription": True,
    },
]


async def seed_medicines(db: AsyncSession) -> None:
    for med_data in SAMPLE_MEDICINES:
        result = await db.execute(
            select(MedicineCatalog).where(
                MedicineCatalog.barcode == med_data["barcode"]
            )
        )
        existing = result.scalar_one_or_none()
        if not existing:
            medicine = MedicineCatalog(
                id=uuid.uuid4(),
                **med_data,
                is_active=True,
            )
            db.add(medicine)
            print(f"Added medicine: {med_data['brand_name']}")
        else:
            print(f"Medicine exists: {med_data['brand_name']}")
    await db.commit()
    print(f"Medicine seeding complete! {len(SAMPLE_MEDICINES)} medicines processed.")


async def run_seeder():
    async with AsyncSessionLocal() as db:
        await seed_medicines(db)


if __name__ == "__main__":
    asyncio.run(run_seeder())
