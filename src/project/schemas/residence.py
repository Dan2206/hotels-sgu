from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime


class ResidenceCreateUpdateSchema(BaseModel):
    hotel: int
    room: int
    main_client: int
    who_buy: int
    booking: int | None = Field(default=None)
    date_of_start: date
    date_of_end: date
    sum_price: int | None = Field(default=None)


class ResidenceSchema(ResidenceCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
