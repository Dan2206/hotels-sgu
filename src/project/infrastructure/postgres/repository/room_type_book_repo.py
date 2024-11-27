from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.room_type_book import RoomTypeBookSchema, RoomTypeBookCreateUpdateSchema
from project.infrastructure.postgres.models import RoomTypeBook

from project.core.config import settings
from project.core.exceptions.room_type_book import RoomTypeBookNotFound


class RoomTypeBookRepository:
    _collection: Type[RoomTypeBook] = RoomTypeBook

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_room_type_books(
        self,
        session: AsyncSession,
    ) -> list[RoomTypeBookSchema]:
        query = select(self._collection)

        room_type_books = await session.scalars(query)
        return [RoomTypeBookSchema.model_validate(obj=room_type_book) for room_type_book in room_type_books.all()]

    async def get_room_type_book_by_id(
            self,
            session: AsyncSession,
            room_type_book_id: int,
    ) -> RoomTypeBookSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == room_type_book_id)
        )
        user = await session.scalar(query)
        if not user:
            raise RoomTypeBookNotFound(_id=room_type_book_id)
        return RoomTypeBookSchema.model_validate(obj=user)

    async def create_room_type_book(
            self,
            session: AsyncSession,
            room_type_book: RoomTypeBookCreateUpdateSchema,
    ) -> RoomTypeBookSchema:
        query = (
            insert(self._collection)
            .values(room_type_book.model_dump())
            .returning(self._collection)
        )
        # try: NO EXCEPTIONS AVAILABLE
        created_room_type_book = await session.scalar(query)
        await session.flush()
        # except IntegrityError as err:
        return RoomTypeBookSchema.model_validate(obj=created_room_type_book)

    async def update_room_type_book(
            self,
            session: AsyncSession,
            room_type_book_id: int,
            room_type_book: RoomTypeBookCreateUpdateSchema,
    ) -> RoomTypeBookSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == room_type_book_id)
            .values(room_type_book.model_dump())
            .returning(self._collection)
        )
        updated_room_type_book = await session.scalar(query)
        if not updated_room_type_book:
            raise RoomTypeBookNotFound(_id=room_type_book_id)
        return RoomTypeBookSchema.model_validate(obj=updated_room_type_book)

    async def delete_room_type_book(
            self,
            session: AsyncSession,
            room_type_book_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == room_type_book_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise RoomTypeBookNotFound(_id=room_type_book_id)

