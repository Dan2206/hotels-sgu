from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.room_type import RoomTypeSchema, RoomTypeCreateUpdateSchema
from project.infrastructure.postgres.models import RoomType

from project.core.config import settings
from project.core.exceptions import RoomTypeNotFound, RoomTypeBadForeignKey, RoomTypeBadDate


class RoomTypeRepository:
    _collection: Type[RoomType] = RoomType

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_room_types(
        self,
        session: AsyncSession,
    ) -> list[RoomTypeSchema]:
        query = select(self._collection)

        room_types = await session.scalars(query)
        return [RoomTypeSchema.model_validate(obj=room_type) for room_type in room_types.all()]

    async def get_room_type_by_id(
            self,
            session: AsyncSession,
            room_type_id: int,
    ) -> RoomTypeSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == room_type_id)
        )
        user = await session.scalar(query)
        if not user:
            raise RoomTypeNotFound(_id=room_type_id)
        return RoomTypeSchema.model_validate(obj=user)

    async def create_room_type(
            self,
            session: AsyncSession,
            room_type: RoomTypeCreateUpdateSchema,
    ) -> RoomTypeSchema:
        query = (
            insert(self._collection)
            .values(room_type.model_dump())
            .returning(self._collection)
        )
        try:
            created_room_type = await session.scalar(query)
            await session.flush()
        except IntegrityError as err:
            if RoomType.check_date_constraint in str(err.orig):
                raise RoomTypeBadDate(date_start=room_type.date_of_start, date_end=room_type.date_of_end)
            else:
                raise RoomTypeBadForeignKey()
        return RoomTypeSchema.model_validate(obj=created_room_type)

    async def update_room_type(
            self,
            session: AsyncSession,
            room_type_id: int,
            room_type: RoomTypeCreateUpdateSchema,
    ) -> RoomTypeSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == room_type_id)
            .values(room_type.model_dump())
            .returning(self._collection)
        )
        updated_room_type = await session.scalar(query)
        if not updated_room_type:
            raise RoomTypeNotFound(_id=room_type_id)
        return RoomTypeSchema.model_validate(obj=updated_room_type)

    async def delete_room_type(
            self,
            session: AsyncSession,
            room_type_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == room_type_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise RoomTypeNotFound(_id=room_type_id)

