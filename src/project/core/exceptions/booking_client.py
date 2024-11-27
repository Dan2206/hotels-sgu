from typing import Final
from datetime import date, datetime


class BookingClientNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Связь бронирования и клиента с id {id} не найдена"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)

class BookingClientBadForeignKey(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "При вставке связи бронирования и клиента нарушены внешние ключи"
    message: str

    def __init__(self) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format()
        super().__init__(self.message)