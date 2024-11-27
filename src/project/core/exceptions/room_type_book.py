from typing import Final
from datetime import date, datetime


class RoomTypeBookNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Категория номера с id {id} не найдена"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)
