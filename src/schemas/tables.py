from pydantic import BaseModel, Field

class TableCreateSchema(BaseModel):
    name: str = Field(min_length=2, max_length=20, default="standard")
    seats: int = Field(ge=1, le=50, default=2)
    location: str = Field(min_length=2, max_length=100, default="in the center of the hall")
    

class TableSchema(TableCreateSchema):
    id: int