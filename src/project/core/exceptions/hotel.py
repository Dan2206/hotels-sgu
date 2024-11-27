from typing import Final
from datetime import date, datetime


class HotelNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Отель с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class HotelStarsIncorrect(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "У отеля не может быть звезд в количестве {stars}"
    message: str

    def __init__(self, stars: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(stars=stars)
        super().__init__(self.message)


class HotelAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Отель с названием '{name}' уже существует"
    message: str

    def __init__(self, name: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(name=name)
        super().__init__(self.message)