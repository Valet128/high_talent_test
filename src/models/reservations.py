from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

class ReservationModel(Base):
    __tablename__ = 'reservations'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(index=True)
    reservation_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[int]
    table_fk: Mapped[int] = mapped_column(ForeignKey(column="tables.id", ondelete="CASCADE"))

    table: Mapped["TableModel"] = relationship(back_populates="reservations", uselist=False)