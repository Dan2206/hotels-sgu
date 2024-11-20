from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime


class ClientSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    surname: str
    name: str
    patronymic: str
    date_of_birth: date
    type_of_document : str
    document : str
    date_of_reg : datetime
    email : str | None = Field(default=None)
    phone : str | None = Field(default=None)