from typing import Final
from datetime import date, datetime


class ServiceAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Услуга с названием '{service_num}' в отеле с id '{hotel}' уже существует"
    message: str

    def __init__(self, name: str, hotel: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(service_name=name, hotel=hotel)
        super().__init__(self.message)


class ServiceNoHotel(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Не существует отеля с id '{hotel}', поэтому невозможно добавить услугу"
    message: str

    def __init__(self, hotel: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(hotel=hotel)
        super().__init__(self.message)


class ServiceNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Услуга с id {id} не найдена"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)
