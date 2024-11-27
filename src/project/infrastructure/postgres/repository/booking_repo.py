from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.booking import BookingSchema, BookingCreateUpdateSchema
from project.infrastructure.postgres.models import Booking

from project.core.config import settings
from project.core.exceptions import BookingNotFound, BookingBadDate, BookingBadForeignKey


class BookingRepository:
    _collection: Type[Booking] = Booking

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_bookings(
        self,
        session: AsyncSession,
    ) -> list[BookingSchema]:
        query = select(self._collection)

        bookings = await session.scalars(query)
        return [BookingSchema.model_validate(obj=booking) for booking in bookings.all()]

    async def get_booking_by_id(
            self,
            session: AsyncSession,
            booking_id: int,
    ) -> BookingSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == booking_id)
        )
        user = await session.scalar(query)
        if not user:
            raise BookingNotFound(_id=booking_id)
        return BookingSchema.model_validate(obj=user)

    async def create_booking(
            self,
            session: AsyncSession,
            booking: BookingCreateUpdateSchema,
    ) -> BookingSchema:
        query = (
            insert(self._collection)
            .values(booking.model_dump())
            .returning(self._collection)
        )
        try:
            created_booking = await session.scalar(query)
            await session.flush()
        except IntegrityError as err:
            if Booking.date_constraint in str(err.orig):
                raise BookingBadDate(date_start=booking.date_of_start, date_end=booking.date_of_end)
            else:
                raise BookingBadForeignKey()
        return BookingSchema.model_validate(obj=created_booking)

    async def update_booking(
            self,
            session: AsyncSession,
            booking_id: int,
            booking: BookingCreateUpdateSchema,
    ) -> BookingSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == booking_id)
            .values(booking.model_dump())
            .returning(self._collection)
        )
        updated_booking = await session.scalar(query)
        if not updated_booking:
            raise BookingNotFound(_id=booking_id)
        return BookingSchema.model_validate(obj=updated_booking)

    async def delete_booking(
            self,
            session: AsyncSession,
            booking_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == booking_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise BookingNotFound(_id=booking_id)

