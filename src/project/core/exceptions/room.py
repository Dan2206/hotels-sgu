from typing import Final
from datetime import date, datetime


class RoomNumAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Комната '{room_num}' в отеле с id '{hotel}' уже существует"
    message: str

    def __init__(self, room_num: int, hotel: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(room_num=room_num, hotel=hotel)
        super().__init__(self.message)


class RoomNoHotel(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Не существует отеля с id '{hotel}', поэтому невозможно добавить комнату"
    message: str

    def __init__(self, hotel: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(hotel=hotel)
        super().__init__(self.message)


class RoomNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Номер с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)
