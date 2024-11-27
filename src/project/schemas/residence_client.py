from pydantic import BaseModel, ConfigDict, Field


class ResidenceClientCreateUpdateSchema(BaseModel):
    residence: int
    client: int


class ResidenceClientSchema(ResidenceClientCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
