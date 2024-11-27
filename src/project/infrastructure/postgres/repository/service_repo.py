from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.service import ServiceSchema, ServiceCreateUpdateSchema
from project.infrastructure.postgres.models import Service

from project.core.config import settings
from project.core.exceptions import ServiceNoHotel, ServiceAlreadyExists, ServiceNotFound


class ServiceRepository:
    _collection: Type[Service] = Service

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_services(
        self,
        session: AsyncSession,
    ) -> list[ServiceSchema]:
        query = select(self._collection)

        services = await session.scalars(query)
        return [ServiceSchema.model_validate(obj=service) for service in services.all()]

    async def get_service_by_id(
            self,
            session: AsyncSession,
            service_id: int,
    ) -> ServiceSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == service_id)
        )
        user = await session.scalar(query)
        if not user:
            raise ServiceNotFound(_id=service_id)
        return ServiceSchema.model_validate(obj=user)

    async def create_service(
            self,
            session: AsyncSession,
            service: ServiceCreateUpdateSchema,
    ) -> ServiceSchema:
        query = (
            insert(self._collection)
            .values(service.model_dump())
            .returning(self._collection)
        )
        try:
            created_service = await session.scalar(query)
            await session.flush()
        except IntegrityError as err:
            if Service.unique_hotel_name_constraint in str(err.orig):
                raise ServiceAlreadyExists(hotel=service.hotel, name=service.name)
            else:
                raise ServiceNoHotel(hotel=service.hotel)
        return ServiceSchema.model_validate(obj=created_service)

    async def update_service(
            self,
            session: AsyncSession,
            service_id: int,
            service: ServiceCreateUpdateSchema,
    ) -> ServiceSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == service_id)
            .values(service.model_dump())
            .returning(self._collection)
        )
        updated_service = await session.scalar(query)
        if not updated_service:
            raise ServiceNotFound(_id=service_id)
        return ServiceSchema.model_validate(obj=updated_service)

    async def delete_service(
            self,
            session: AsyncSession,
            service_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == service_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise ServiceNotFound(_id=service_id)

