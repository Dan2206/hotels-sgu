from typing import Final
from datetime import date, datetime


class RoomTypeNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Запись о номере и его категории с id {id} не найдена"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class RoomTypeBadForeignKey(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Нарушен внешний ключ при добавлении записи о номере и его категории"
    message: str

    def __init__(self) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format()
        super().__init__(self.message)


class RoomTypeBadDate(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] =\
        "Период действия записи о номере и его категории не может начаться ({ds}) позже, чем закончиться ({de})"
    message: str

    def __init__(self, date_start: date, date_end: date) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(ds=date_start, de=date_end)
        super().__init__(self.message)