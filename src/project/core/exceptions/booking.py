from typing import Final
from datetime import date, datetime


class BookingNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Бронирование с id {id} не найдено"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class BookingBadForeignKey(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Нарушен внешний ключ при добавлении бронирования"
    message: str

    def __init__(self) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format()
        super().__init__(self.message)


class BookingBadDate(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Бронирование не может начаться ({ds}) позже, чем закончиться ({de})"
    message: str

    def __init__(self, date_start: date, date_end: date) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(ds=date_start, de=date_end)
        super().__init__(self.message)
