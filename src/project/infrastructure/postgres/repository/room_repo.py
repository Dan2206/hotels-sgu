from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.room import RoomSchema, RoomCreateUpdateSchema
from project.infrastructure.postgres.models import Room

from project.core.config import settings
from project.core.exceptions import RoomNoHotel, RoomNumAlreadyExists, RoomNotFound


class RoomRepository:
    _collection: Type[Room] = Room

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_rooms(
        self,
        session: AsyncSession,
    ) -> list[RoomSchema]:
        query = select(self._collection)

        rooms = await session.scalars(query)
        return [RoomSchema.model_validate(obj=room) for room in rooms.all()]

    async def get_room_by_id(
            self,
            session: AsyncSession,
            room_id: int,
    ) -> RoomSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == room_id)
        )
        user = await session.scalar(query)
        if not user:
            raise RoomNotFound(_id=room_id)
        return RoomSchema.model_validate(obj=user)

    async def create_room(
            self,
            session: AsyncSession,
            room: RoomCreateUpdateSchema,
    ) -> RoomSchema:
        query = (
            insert(self._collection)
            .values(room.model_dump())
            .returning(self._collection)
        )
        try:
            created_room = await session.scalar(query)
            await session.flush()
        except IntegrityError as err:
            if Room.unique_room_num_constraint in str(err.orig):
                raise RoomNumAlreadyExists(hotel=room.hotel, room_num=room.room_num)
            else:
                raise RoomNoHotel(hotel=room.hotel)
        return RoomSchema.model_validate(obj=created_room)

    async def update_room(
            self,
            session: AsyncSession,
            room_id: int,
            room: RoomCreateUpdateSchema,
    ) -> RoomSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == room_id)
            .values(room.model_dump())
            .returning(self._collection)
        )
        updated_room = await session.scalar(query)
        if not updated_room:
            raise RoomNotFound(_id=room_id)
        return RoomSchema.model_validate(obj=updated_room)

    async def delete_room(
            self,
            session: AsyncSession,
            room_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == room_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise RoomNotFound(_id=room_id)

