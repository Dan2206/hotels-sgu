from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.residence import ResidenceSchema, ResidenceCreateUpdateSchema
from project.infrastructure.postgres.models import Residence

from project.core.config import settings
from project.core.exceptions import ResidenceNotFound, ResidenceBadDate, ResidenceBadForeignKey


class ResidenceRepository:
    _collection: Type[Residence] = Residence

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_residences(
        self,
        session: AsyncSession,
    ) -> list[ResidenceSchema]:
        query = select(self._collection)

        residences = await session.scalars(query)
        return [ResidenceSchema.model_validate(obj=residence) for residence in residences.all()]

    async def get_residence_by_id(
            self,
            session: AsyncSession,
            residence_id: int,
    ) -> ResidenceSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == residence_id)
        )
        user = await session.scalar(query)
        if not user:
            raise ResidenceNotFound(_id=residence_id)
        return ResidenceSchema.model_validate(obj=user)

    async def create_residence(
            self,
            session: AsyncSession,
            residence: ResidenceCreateUpdateSchema,
    ) -> ResidenceSchema:
        query = (
            insert(self._collection)
            .values(residence.model_dump())
            .returning(self._collection)
        )
        try:
            created_residence = await session.scalar(query)
            await session.flush()
        except IntegrityError as err:
            if Residence.date_constraint in str(err.orig):
                raise ResidenceBadDate(date_start=residence.date_of_start, date_end=residence.date_of_end)
            else:
                raise ResidenceBadForeignKey()
        return ResidenceSchema.model_validate(obj=created_residence)

    async def update_residence(
            self,
            session: AsyncSession,
            residence_id: int,
            residence: ResidenceCreateUpdateSchema,
    ) -> ResidenceSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == residence_id)
            .values(residence.model_dump())
            .returning(self._collection)
        )
        updated_residence = await session.scalar(query)
        if not updated_residence:
            raise ResidenceNotFound(_id=residence_id)
        return ResidenceSchema.model_validate(obj=updated_residence)

    async def delete_residence(
            self,
            session: AsyncSession,
            residence_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == residence_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise ResidenceNotFound(_id=residence_id)

