from fastapi import APIRouter
from sqlalchemy import select, delete 
from sqlalchemy.orm import selectinload

from src.models.tables import TableModel
from src.dependencies import SessionDep
from src.schemas.tables import TableSchema


router = APIRouter()

@router.get('/tables/', tags=["Tables"])
async def get_tables(session: SessionDep):
    query = select(TableModel).options(selectinload(TableModel.reservations))
    result = await session.execute(query)
    
    return {"response": result.scalars().all()}
    
@router.post('/tables/', tags=["Tables"])
async def create_table(table: TableSchema, session: SessionDep):
    new_table = TableModel(
        name=table.name,
        seats=table.seats,
        location=table.location,
    )
    session.add(new_table)
    await session.commit()

    return {"response": "Table has been added"}
    
@router.delete('/tables/', tags=["Tables"])
async def delete_table(id: int, session: SessionDep):
    
    table_query = select(TableModel).where(TableModel.id == id)
    table = await session.execute(table_query)
    
    if table.first() == None:
        return {"response": "Table not found"}

    query = delete(TableModel).where(id == TableModel.id)
    await session.execute(query)
    await session.commit()
    return {"response": "Table has been deleted"}