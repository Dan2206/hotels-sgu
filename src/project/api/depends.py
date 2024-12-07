from typing import Annotated

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status

from project.schemas.auth import TokenData
from project.schemas.user import UserSchema
from project.core.config import settings
from project.core.exceptions.auth import CredentialsException
from project.resource.auth import oauth2_scheme

from project.infrastructure.postgres.repository.client_repo import ClientRepository
from project.infrastructure.postgres.repository.hotel_repo import HotelRepository
from project.infrastructure.postgres.repository.room_repo import RoomRepository
from project.infrastructure.postgres.repository.room_type_book_repo import RoomTypeBookRepository
from project.infrastructure.postgres.repository.room_type_repo import RoomTypeRepository
from project.infrastructure.postgres.repository.price_repo import PriceRepository
from project.infrastructure.postgres.repository.buyer_repo import BuyerRepository
from project.infrastructure.postgres.repository.booking_repo import BookingRepository
from project.infrastructure.postgres.repository.booking_client_repo import BookingClientRepository
from project.infrastructure.postgres.repository.residence_repo import ResidenceRepository
from project.infrastructure.postgres.repository.residence_client_repo import ResidenceClientRepository
from project.infrastructure.postgres.repository.service_repo import ServiceRepository
from project.infrastructure.postgres.repository.service_rendered_repo import ServiceRenderedRepository
from project.infrastructure.postgres.repository.price_service_repo import PriceServiceRepository
from project.infrastructure.postgres.repository.user_repo import UserRepository
from project.infrastructure.postgres.database import PostgresDatabase

client_repo = ClientRepository()
hotel_repo = HotelRepository()
room_repo = RoomRepository()
room_type_book_repo = RoomTypeBookRepository()
room_type_repo = RoomTypeRepository()
price_repo = PriceRepository()
buyer_repo = BuyerRepository()
booking_repo = BookingRepository()
booking_client_repo = BookingClientRepository()
residence_repo = ResidenceRepository()
residence_client_repo = ResidenceClientRepository()
service_repo = ServiceRepository()
service_rendered_repo = ServiceRenderedRepository()
price_service_repo = PriceServiceRepository()
user_repo = UserRepository()
database = PostgresDatabase()

AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные для авторизации"


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithms=[settings.AUTH_ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

    async with database.session() as session:
        user = await user_repo.get_user_by_email(
            session=session,
            email=token_data.username,
        )

    if user is None:
        raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

    return user


def check_for_admin_access(user: UserSchema) -> None:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только админ имеет права добавлять/изменять/удалять в данной таблице"
        )
