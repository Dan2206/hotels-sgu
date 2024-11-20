from pydantic import BaseModel, ConfigDict


class HotelCreateUpdateSchema(BaseModel):
    name: str
    address: str
    stars: int


class HotelSchema(HotelCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
