from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.buyer import BuyerSchema, BuyerCreateUpdateSchema
from project.infrastructure.postgres.models import Buyer

from project.core.config import settings
from project.core.exceptions import BuyerNotFound


class BuyerRepository:
    _collection: Type[Buyer] = Buyer

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_buyers(
        self,
        session: AsyncSession,
    ) -> list[BuyerSchema]:
        query = select(self._collection)

        buyers = await session.scalars(query)
        return [BuyerSchema.model_validate(obj=buyer) for buyer in buyers.all()]

    async def get_buyer_by_id(
            self,
            session: AsyncSession,
            buyer_id: int,
    ) -> BuyerSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == buyer_id)
        )
        user = await session.scalar(query)
        if not user:
            raise BuyerNotFound(_id=buyer_id)
        return BuyerSchema.model_validate(obj=user)

    async def create_buyer(
            self,
            session: AsyncSession,
            buyer: BuyerCreateUpdateSchema,
    ) -> BuyerSchema:
        query = (
            insert(self._collection)
            .values(buyer.model_dump())
            .returning(self._collection)
        )
        #try:
        created_buyer = await session.scalar(query)
        await session.flush()
        # except IntegrityError as err:
        #    raise
        # TODO проверки вроде не нужны, но...
        return BuyerSchema.model_validate(obj=created_buyer)

    async def update_buyer(
            self,
            session: AsyncSession,
            buyer_id: int,
            buyer: BuyerCreateUpdateSchema,
    ) -> BuyerSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == buyer_id)
            .values(buyer.model_dump())
            .returning(self._collection)
        )
        updated_buyer = await session.scalar(query)
        if not updated_buyer:
            raise BuyerNotFound(_id=buyer_id)
        return BuyerSchema.model_validate(obj=updated_buyer)

    async def delete_buyer(
            self,
            session: AsyncSession,
            buyer_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == buyer_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise BuyerNotFound(_id=buyer_id)

