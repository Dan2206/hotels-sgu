from pydantic import BaseModel, ConfigDict, Field


class BuyerCreateUpdateSchema(BaseModel):
    is_company: bool
    name: str
    email: str | None = Field(default=None)
    phone: str


class BuyerSchema(BuyerCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
