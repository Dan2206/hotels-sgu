from typing import Final
from datetime import date, datetime


class ServiceRenderedNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Запись об оказании услуги с id {id} не найдена"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class ServiceRenderedBadForeignKey(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Нарушен внешний ключ при добавлении записи об оказании услуги"
    message: str

    def __init__(self) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format()
        super().__init__(self.message)
