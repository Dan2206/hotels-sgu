from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime


class PriceCreateUpdateSchema(BaseModel):
    hotel: int
    category: int
    price: int
    date_of_start: date
    date_of_end: date


class PriceSchema(PriceCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
