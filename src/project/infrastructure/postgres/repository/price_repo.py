from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.price import PriceSchema, PriceCreateUpdateSchema
from project.infrastructure.postgres.models import Price

from project.core.config import settings
from project.core.exceptions.price import PriceNotFound, PriceBadForeignKey, PriceBadPrice, PriceBadDate


class PriceRepository:
    _collection: Type[Price] = Price

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_prices(
        self,
        session: AsyncSession,
    ) -> list[PriceSchema]:
        query = select(self._collection)

        prices = await session.scalars(query)
        return [PriceSchema.model_validate(obj=price) for price in prices.all()]

    async def get_price_by_id(
            self,
            session: AsyncSession,
            price_id: int,
    ) -> PriceSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == price_id)
        )
        user = await session.scalar(query)
        if not user:
            raise PriceNotFound(_id=price_id)
        return PriceSchema.model_validate(obj=user)

    async def create_price(
            self,
            session: AsyncSession,
            price: PriceCreateUpdateSchema,
    ) -> PriceSchema:
        query = (
            insert(self._collection)
            .values(price.model_dump())
            .returning(self._collection)
        )
        try:
            created_price = await session.scalar(query)
            await session.flush()
        except IntegrityError as err:
            if Price.check_price_constraint in str(err.orig):
                raise PriceBadPrice(price_value=price.price)
            elif Price.check_date_constraint in str(err.orig):
                raise PriceBadDate(date_start=price.date_of_start, date_end=price.date_of_end)
            else:
                raise PriceBadForeignKey()
        return PriceSchema.model_validate(obj=created_price)

    async def update_price(
            self,
            session: AsyncSession,
            price_id: int,
            price: PriceCreateUpdateSchema,
    ) -> PriceSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == price_id)
            .values(price.model_dump())
            .returning(self._collection)
        )
        updated_price = await session.scalar(query)
        if not updated_price:
            raise PriceNotFound(_id=price_id)
        return PriceSchema.model_validate(obj=updated_price)

    async def delete_price(
            self,
            session: AsyncSession,
            price_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == price_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise PriceNotFound(_id=price_id)

