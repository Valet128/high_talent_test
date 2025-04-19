from fastapi import APIRouter

from src.database import Base, engine

router = APIRouter()

@router.post('/setup_database/', tags=["Setup Database"], summary="Drop all tables in database and create all new tables")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"response": "Database updated"}
