from pydantic import BaseModel, ConfigDict, Field


class RoomTypeBookCreateUpdateSchema(BaseModel):
    name: str
    places: int
    square: int
    extra_places: int
    description: str | None = Field(default=None)


class RoomTypeBookSchema(RoomTypeBookCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
