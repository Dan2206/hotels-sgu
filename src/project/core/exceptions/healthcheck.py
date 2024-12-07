from typing import Final


class DatabaseError(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Произошла ошибка в базе данных: {message}"

    def __init__(self, message: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(message=message)
        super().__init__(self.message)