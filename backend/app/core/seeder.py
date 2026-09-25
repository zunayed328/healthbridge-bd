import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.user import Role

DEFAULT_ROLES = [
    {
        "name": "patient",
        "description": "Regular patient user",
    },
    {
        "name": "doctor",
        "description": "Verified medical doctor",
    },
    {
        "name": "pharmacy",
        "description": "Pharmacy staff or owner",
    },
    {
        "name": "admin",
        "description": "Platform administrator",
    },
]


async def seed_roles(db: AsyncSession) -> None:
    for role_data in DEFAULT_ROLES:
        result = await db.execute(
            select(Role).where(Role.name == role_data["name"])
        )
        existing = result.scalar_one_or_none()
        if not existing:
            role = Role(
                id=uuid.uuid4(),
                name=role_data["name"],
                description=role_data["description"],
            )
            db.add(role)
            print(f"Created role: {role_data['name']}")
        else:
            print(f"Role already exists: {role_data['name']}")
    await db.commit()
    print("Roles seeding complete!")


async def run_seeder():
    async with AsyncSessionLocal() as db:
        await seed_roles(db)


if __name__ == "__main__":
    asyncio.run(run_seeder())
