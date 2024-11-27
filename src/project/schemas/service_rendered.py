from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime


class ServiceRenderedCreateUpdateSchema(BaseModel):
    service: int
    client: int
    is_rendered: bool
    date_of_render: datetime


class SerivceRenderedSchema(ServiceRenderedCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
