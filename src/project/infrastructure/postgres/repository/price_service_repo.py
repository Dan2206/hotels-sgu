from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.price_service import PriceServiceSchema, PriceServiceCreateUpdateSchema
from project.infrastructure.postgres.models import PriceService

from project.core.config import settings
from project.core.exceptions import PriceNotFound, PriceBadForeignKey, PriceBadPrice, PriceBadDate


class PriceServiceRepository:
    _collection: Type[PriceService] = PriceService

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_price_services(
        self,
        session: AsyncSession,
    ) -> list[PriceServiceSchema]:
        query = select(self._collection)

        price_services = await session.scalars(query)
        return [PriceServiceSchema.model_validate(obj=price_service) for price_service in price_services.all()]

    async def get_price_service_by_id(
            self,
            session: AsyncSession,
            price_service_id: int,
    ) -> PriceServiceSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == price_service_id)
        )
        user = await session.scalar(query)
        if not user:
            raise PriceNotFound(_id=price_service_id)
        return PriceServiceSchema.model_validate(obj=user)

    async def create_price_service(
            self,
            session: AsyncSession,
            price_service: PriceServiceCreateUpdateSchema,
    ) -> PriceServiceSchema:
        query = (
            insert(self._collection)
            .values(price_service.model_dump())
            .returning(self._collection)
        )
        try:
            created_price_service = await session.scalar(query)
            await session.flush()
        except IntegrityError as err:
            if PriceService.check_price_constraint in str(err.orig):
                raise PriceBadPrice(price_value=price_service.price)
            elif PriceService.check_date_constraint in str(err.orig):
                raise PriceBadDate(date_start=price_service.date_of_start, date_end=price_service.date_of_end)
            else:
                raise PriceBadForeignKey()
        return PriceServiceSchema.model_validate(obj=created_price_service)

    async def update_price_service(
            self,
            session: AsyncSession,
            price_service_id: int,
            price_service: PriceServiceCreateUpdateSchema,
    ) -> PriceServiceSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == price_service_id)
            .values(price_service.model_dump())
            .returning(self._collection)
        )
        updated_price_service = await session.scalar(query)
        if not updated_price_service:
            raise PriceNotFound(_id=price_service_id)
        return PriceServiceSchema.model_validate(obj=updated_price_service)

    async def delete_price_service(
            self,
            session: AsyncSession,
            price_service_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == price_service_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise PriceNotFound(_id=price_service_id)

