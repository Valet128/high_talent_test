from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

class TableModel(Base):
    __tablename__ = 'tables'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    seats: Mapped[int]
    location: Mapped[str]
    
    reservations: Mapped[list["ReservationModel"]] = relationship(back_populates="table", uselist=True)