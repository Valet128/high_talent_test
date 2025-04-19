from datetime import datetime
from pydantic import BaseModel, Field


class ReservationCreateSchema(BaseModel):
    customer_name: str = Field(min_length=2, max_length=20)
    table_fk: int = Field(ge=1, le=1000)
    reservation_time: datetime = Field(default=datetime.now())
    duration_minutes: int = Field(ge=1, le=480, default=1)

class ReservationSchema(ReservationCreateSchema):
    id: int
