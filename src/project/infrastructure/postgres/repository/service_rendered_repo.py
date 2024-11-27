from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.service_rendered import ServiceRenderedSchema, ServiceRenderedCreateUpdateSchema
from project.infrastructure.postgres.models import ServiceRendered

from project.core.config import settings
from project.core.exceptions.service_rendered import ServiceRenderedBadForeignKey, ServiceRenderedNotFound


class ServiceRenderedRepository:
    _collection: Type[ServiceRendered] = ServiceRendered

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_service_rendereds(
        self,
        session: AsyncSession,
    ) -> list[ServiceRenderedSchema]:
        query = select(self._collection)

        service_rendereds = await session.scalars(query)
        return [ServiceRenderedSchema.model_validate(obj=service_rendered) for service_rendered in service_rendereds.all()]

    async def get_service_rendered_by_id(
            self,
            session: AsyncSession,
            service_rendered_id: int,
    ) -> ServiceRenderedSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == service_rendered_id)
        )
        user = await session.scalar(query)
        if not user:
            raise ServiceRenderedNotFound(_id=service_rendered_id)
        return ServiceRenderedSchema.model_validate(obj=user)

    async def create_service_rendered(
            self,
            session: AsyncSession,
            service_rendered: ServiceRenderedCreateUpdateSchema,
    ) -> ServiceRenderedSchema:
        query = (
            insert(self._collection)
            .values(service_rendered.model_dump())
            .returning(self._collection)
        )
        try:
            created_service_rendered = await session.scalar(query)
            await session.flush()
        except IntegrityError as err:
            raise ServiceRenderedBadForeignKey()
        return ServiceRenderedSchema.model_validate(obj=created_service_rendered)

    async def update_service_rendered(
            self,
            session: AsyncSession,
            service_rendered_id: int,
            service_rendered: ServiceRenderedCreateUpdateSchema,
    ) -> ServiceRenderedSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == service_rendered_id)
            .values(service_rendered.model_dump())
            .returning(self._collection)
        )
        updated_service_rendered = await session.scalar(query)
        if not updated_service_rendered:
            raise ServiceRenderedNotFound(_id=service_rendered_id)
        return ServiceRenderedSchema.model_validate(obj=updated_service_rendered)

    async def delete_service_rendered(
            self,
            session: AsyncSession,
            service_rendered_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == service_rendered_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise ServiceRenderedNotFound(_id=service_rendered_id)

