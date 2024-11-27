from typing import Final
from datetime import date, datetime


class ClientNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Клиент с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class ClientAlreadyExistsEmail(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Клиент с почтой '{email}' уже существует"

    def __init__(self, email: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(email=email)
        super().__init__(self.message)


class ClientAlreadyExistsDoc(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Клиент с документом '{doc}' типа '{type_doc}' уже существует"

    def __init__(self, doc: str, type_doc: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(doc=doc, type_doc=type_doc)
        super().__init__(self.message)


class ClientAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Клиент уже существует"

    def __init__(self) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format()
        super().__init__(self.message)


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


class BuyerNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Покупатель с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


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


class BookingClientNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Связь бронирования и клиента с id {id} не найдена"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


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


class ResidenceClientNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Запись о проживании с id {id} не найдена"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


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


class RoomTypeBookNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Категория номера с id {id} не найдена"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


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