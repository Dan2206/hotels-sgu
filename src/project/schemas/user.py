from pydantic import BaseModel, ConfigDict, Field


class UserCreateUpdateSchema(BaseModel):
    surname: str
    name: str
    patronymic: str
    is_admin: bool = False
    email: str = Field(pattern=r"^\S+@\S+\.\S+$", examples=["email@mail.ru"])
    password: str
    phone_number: str | None = Field(default=None, pattern=r"^\+?7\d{10}$", examples=["+79999999999"])


class UserSchema(UserCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
