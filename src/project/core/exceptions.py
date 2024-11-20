from typing import Final


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