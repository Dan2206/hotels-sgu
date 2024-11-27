from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.booking_client import BookingClientSchema, BookingClientCreateUpdateSchema
from project.infrastructure.postgres.models import BookingClient

from project.core.config import settings
from project.core.exceptions import BookingClientNotFound


class BookingClientRepository:
    _collection: Type[BookingClient] = BookingClient

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_booking_clients(
        self,
        session: AsyncSession,
    ) -> list[BookingClientSchema]:
        query = select(self._collection)

        booking_clients = await session.scalars(query)
        return [BookingClientSchema.model_validate(obj=booking_client) for booking_client in booking_clients.all()]

    async def get_booking_client_by_id(
            self,
            session: AsyncSession,
            booking_client_id: int,
    ) -> BookingClientSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == booking_client_id)
        )
        user = await session.scalar(query)
        if not user:
            raise BookingClientNotFound(_id=booking_client_id)
        return BookingClientSchema.model_validate(obj=user)

    async def create_booking_client(
            self,
            session: AsyncSession,
            booking_client: BookingClientCreateUpdateSchema,
    ) -> BookingClientSchema:
        query = (
            insert(self._collection)
            .values(booking_client.model_dump())
            .returning(self._collection)
        )
        # try: NO ERRORS AVAILABLE
        created_booking_client = await session.scalar(query)
        await session.flush()
        # except IntegrityError as err:
        #     raise
        return BookingClientSchema.model_validate(obj=created_booking_client)

    async def update_booking_client(
            self,
            session: AsyncSession,
            booking_client_id: int,
            booking_client: BookingClientCreateUpdateSchema,
    ) -> BookingClientSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == booking_client_id)
            .values(booking_client.model_dump())
            .returning(self._collection)
        )
        updated_booking_client = await session.scalar(query)
        if not updated_booking_client:
            raise BookingClientNotFound(_id=booking_client_id)
        return BookingClientSchema.model_validate(obj=updated_booking_client)

    async def delete_booking_client(
            self,
            session: AsyncSession,
            booking_client_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == booking_client_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise BookingClientNotFound(_id=booking_client_id)

