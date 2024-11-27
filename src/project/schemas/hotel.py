from pydantic import BaseModel, ConfigDict, Field


class HotelCreateUpdateSchema(BaseModel):
    name: str
    address: str
    stars: int = Field(..., ge=0, le=5)


class HotelSchema(HotelCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
