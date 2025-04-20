from fastapi import APIRouter
from sqlalchemy import select, delete
import time

from src.models.reservations import ReservationModel
from src.models.tables import TableModel
from src.dependencies import SessionDep
from src.schemas.reservations import ReservationSchema


router = APIRouter()

@router.get('/reservations/', tags=["Reservations"])
async def get_reservations(session: SessionDep):
    query = select(ReservationModel)
    result = await session.execute(query)
    
    r_list = result.scalars().all()
    new_r_list = []
    for r in r_list:
        if r.reservation_time.timestamp()+r.duration_minutes*60 < time.time():
            #delete old reservation
            query = delete(ReservationModel).where(ReservationModel.id == r.id)
            await session.execute(query)
            await session.commit()
        else:
            new_r_list.append(r)

    
    return {"response": [r.__dict__ for r in new_r_list]}

@router.post('/reservations/', tags=["Reservations"])
async def create_reservation(reservation: ReservationSchema, session: SessionDep):
    table_query = select(TableModel).where(TableModel.id == reservation.table_fk)
    table = await session.execute(table_query)
    if table.first() == None:
        return {"response": "Table not found"}
    #get object reservation to check up
    reservation_query = select(ReservationModel).where(ReservationModel.table_fk == reservation.table_fk)
    reservation_result = await session.execute(reservation_query)
    r_list = reservation_result.scalars().all()
    
    if r_list:
        # check time reservation on this table
        start_time = reservation.reservation_time.timestamp()
        end_time = reservation.reservation_time.timestamp() + reservation.duration_minutes*60
        for r in r_list:
            if r.reservation_time.timestamp() <= start_time and r.reservation_time.timestamp()+r.duration_minutes*60 >= start_time \
                or end_time >= r.reservation_time.timestamp() and start_time <= r.reservation_time.timestamp():
                return {"response": f"Table already reserved, You could reserve it another time"}

            if r.reservation_time.timestamp()+r.duration_minutes*60 < time.time():
            #delete old reservation
                query = delete(ReservationModel).where(ReservationModel.id == r.id)
                await session.execute(query)
                await session.commit()
        

        #create new_reservation
        if reservation.reservation_time.timestamp() < time.time():
            return {"response": f"You can't reserve table in the past, change time reservation"}

        new_reservation = ReservationModel(
            customer_name=reservation.customer_name,
            table_fk=reservation.table_fk,
            reservation_time=reservation.reservation_time,
            duration_minutes=reservation.duration_minutes,
        )
        session.add(new_reservation)
        await session.commit()
        
        return {"response": "Reservation has been added"}
    else:
        if reservation.reservation_time.timestamp() < time.time():
            return {"response": f"You can't reserve table in the past, change time reservation"}
        new_reservation = ReservationModel(
            customer_name=reservation.customer_name,
            table_fk=reservation.table_fk,
            reservation_time=reservation.reservation_time,
            duration_minutes=reservation.duration_minutes,
        )

        session.add(new_reservation)
        await session.commit()
        
        return {"response": "Reservation has been added"}

@router.delete('/reservations/', tags=["Reservations"])
async def delete_reservation(id: int, session: SessionDep):
    if id < 1:
        return {"response": "Enter a positive number"}
    reservation_query = select(ReservationModel).where(ReservationModel.id == id)
    reservation = await session.execute(reservation_query)
    
    if reservation.first() == None:
        return {"response": "Reservation not found"}

    query = delete(ReservationModel).where(id == ReservationModel.id)
    await session.execute(query)
    await session.commit()
    return {"response": "Reservation has been deleted"}

    