from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime


class PriceServiceCreateUpdateSchema(BaseModel):
    service: int
    date_of_start: date
    date_of_end: date
    price: int = Field(..., gt=0)


class PriceServiceSchema(PriceServiceCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
