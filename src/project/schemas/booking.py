from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime


class BookingCreateUpdateSchema(BaseModel):
    hotel: int
    room_type: int
    who_buy: int
    main_client: int
    date_of_booking: datetime
    date_of_start: date
    date_of_end: date
    extra: str | None = Field(default=None)
    reason_cancel: str | None = Field(default=None)


class BookingSchema(BookingCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
