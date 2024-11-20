from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime


class ClientCreateUpdateSchema(BaseModel):
    surname: str
    name: str
    patronymic: str
    date_of_birth: date
    type_of_document: str
    document: str
    email: str
    phone: str | None = Field(default=None)


class ClientSchema(ClientCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_of_reg: datetime
