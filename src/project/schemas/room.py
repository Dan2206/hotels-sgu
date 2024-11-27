from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime


class RoomCreateUpdateSchema(BaseModel):
    room_num: int
    hotel: int
    active: bool


class RoomSchema(RoomCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
