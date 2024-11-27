from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.hotel import HotelSchema, HotelCreateUpdateSchema
from project.infrastructure.postgres.models import Hotel

from project.core.config import settings
from project.core.exceptions.hotel import HotelNotFound, HotelStarsIncorrect, HotelAlreadyExists


class HotelRepository:
    _collection: Type[Hotel] = Hotel

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_hotels(
        self,
        session: AsyncSession,
    ) -> list[HotelSchema]:
        query = select(self._collection)

        hotels = await session.scalars(query)
        return [HotelSchema.model_validate(obj=hotel) for hotel in hotels.all()]

    async def get_hotel_by_id(
            self,
            session: AsyncSession,
            hotel_id: int,
    ) -> HotelSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == hotel_id)
        )
        user = await session.scalar(query)
        if not user:
            raise HotelNotFound(_id=hotel_id)
        return HotelSchema.model_validate(obj=user)

    async def create_hotel(
            self,
            session: AsyncSession,
            hotel: HotelCreateUpdateSchema,
    ) -> HotelSchema:
        query = (
            insert(self._collection)
            .values(hotel.model_dump())
            .returning(self._collection)
        )
        try:
            created_hotel = await session.scalar(query)
            await session.flush()
        except IntegrityError as err:
            if Hotel.unique_name_constraint in str(err.orig):
                raise HotelAlreadyExists(name=hotel.name)
            else:
                raise HotelStarsIncorrect(stars=hotel.stars)
        return HotelSchema.model_validate(obj=created_hotel)

    async def update_hotel(
            self,
            session: AsyncSession,
            hotel_id: int,
            hotel: HotelCreateUpdateSchema,
    ) -> HotelSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == hotel_id)
            .values(hotel.model_dump())
            .returning(self._collection)
        )
        updated_hotel = await session.scalar(query)
        if not updated_hotel:
            raise HotelNotFound(_id=hotel_id)
        return HotelSchema.model_validate(obj=updated_hotel)

    async def delete_hotel(
            self,
            session: AsyncSession,
            hotel_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == hotel_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise HotelNotFound(_id=hotel_id)

