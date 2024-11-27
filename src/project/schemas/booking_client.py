from pydantic import BaseModel, ConfigDict, Field


class BookingClientCreateUpdateSchema(BaseModel):
    booking: int
    client: int


class BookingClientSchema(BookingClientCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
