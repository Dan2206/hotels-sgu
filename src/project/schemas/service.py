from pydantic import BaseModel, ConfigDict, Field


class ServiceCreateUpdateSchema(BaseModel):
    name: str
    hotel: int
    is_active: bool


class ServiceSchema(ServiceCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
