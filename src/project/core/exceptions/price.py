from typing import Final
from datetime import date, datetime


class PriceNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Запись о цене с id {id} не найдена"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class PriceBadForeignKey(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Нарушен внешний ключ при добавлении записи о цене"
    message: str

    def __init__(self) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format()
        super().__init__(self.message)


class PriceBadDate(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Запись о цене не может начаться ({ds}) позже, чем закончиться ({de})"
    message: str

    def __init__(self, date_start: date, date_end: date) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(ds=date_start, de=date_end)
        super().__init__(self.message)


class PriceBadPrice(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Цена {pr} не явлется положительным числом"
    message: str

    def __init__(self, price_value: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(pr=price_value)
        super().__init__(self.message)
