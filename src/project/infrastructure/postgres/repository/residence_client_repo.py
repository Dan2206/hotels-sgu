from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.residence_client import ResidenceClientSchema, ResidenceClientCreateUpdateSchema
from project.infrastructure.postgres.models import ResidenceClient

from project.core.config import settings
from project.core.exceptions.residence_client import ResidenceClientNotFound, ResidenceClientBadForeignKey


class ResidenceClientRepository:
    _collection: Type[ResidenceClient] = ResidenceClient

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_residence_clients(
        self,
        session: AsyncSession,
    ) -> list[ResidenceClientSchema]:
        query = select(self._collection)

        residence_clients = await session.scalars(query)
        return [ResidenceClientSchema.model_validate(obj=residence_client) for residence_client in residence_clients.all()]

    async def get_residence_client_by_id(
            self,
            session: AsyncSession,
            residence_client_id: int,
    ) -> ResidenceClientSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == residence_client_id)
        )
        user = await session.scalar(query)
        if not user:
            raise ResidenceClientNotFound(_id=residence_client_id)
        return ResidenceClientSchema.model_validate(obj=user)

    async def create_residence_client(
            self,
            session: AsyncSession,
            residence_client: ResidenceClientCreateUpdateSchema,
    ) -> ResidenceClientSchema:
        query = (
            insert(self._collection)
            .values(residence_client.model_dump())
            .returning(self._collection)
        )
        try:
            created_residence_client = await session.scalar(query)
            await session.flush()
        except IntegrityError as err:
            raise ResidenceClientBadForeignKey()
        return ResidenceClientSchema.model_validate(obj=created_residence_client)

    async def update_residence_client(
            self,
            session: AsyncSession,
            residence_client_id: int,
            residence_client: ResidenceClientCreateUpdateSchema,
    ) -> ResidenceClientSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == residence_client_id)
            .values(residence_client.model_dump())
            .returning(self._collection)
        )
        updated_residence_client = await session.scalar(query)
        if not updated_residence_client:
            raise ResidenceClientNotFound(_id=residence_client_id)
        return ResidenceClientSchema.model_validate(obj=updated_residence_client)

    async def delete_residence_client(
            self,
            session: AsyncSession,
            residence_client_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == residence_client_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise ResidenceClientNotFound(_id=residence_client_id)

