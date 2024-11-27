from typing import Final
from datetime import date, datetime


class ResidenceNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Проживание с id {id} не найдено"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class ResidenceBadForeignKey(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Нарушен внешний ключ при добавлении проживания"
    message: str

    def __init__(self) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format()
        super().__init__(self.message)


class ResidenceBadDate(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Проживание не может начаться ({ds}) позже, чем закончиться ({de})"
    message: str

    def __init__(self, date_start: date, date_end: date) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(ds=date_start, de=date_end)
        super().__init__(self.message)