from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime


class RoomTypeCreateUpdateSchema(BaseModel):
    room: int
    category: int
    date_of_start: date
    date_of_end: date


class RoomTypeSchema(RoomTypeCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
