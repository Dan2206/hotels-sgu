from fastapi import APIRouter, HTTPException, status

from project.schemas.residence import ResidenceSchema, ResidenceCreateUpdateSchema
from project.core.exceptions.residence import ResidenceNotFound, ResidenceBadForeignKey, ResidenceBadDate
from project.api.depends import database, residence_repo

router = APIRouter()


@router.get("/all_residences", response_model=list[ResidenceSchema], status_code=status.HTTP_200_OK)
async def get_all_residences() -> list[ResidenceSchema]:
    async with database.session() as session:
        all_residences = await residence_repo.get_all_residences(session=session)

    return all_residences


@router.get("/residence/{residence_id}", response_model=ResidenceSchema, status_code=status.HTTP_200_OK)
async def get_residence_by_id(
    residence_id: int,
) -> ResidenceSchema:
    try:
        async with database.session() as session:
            residence = await residence_repo.get_residence_by_id(session=session, residence_id=residence_id)
    except ResidenceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return residence


@router.post("/add_residence", response_model=ResidenceSchema, status_code=status.HTTP_201_CREATED)
async def add_residence(
    residence_dto: ResidenceCreateUpdateSchema,
) -> ResidenceSchema:
    try:
        async with database.session() as session:
            new_residence = await residence_repo.create_residence(session=session, residence=residence_dto)
    except (ResidenceBadForeignKey, ResidenceBadDate) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    return new_residence


@router.put(
    "/update_residence/{residence_id}",
    response_model=ResidenceSchema,
    status_code=status.HTTP_200_OK,
)
async def update_residence(
    residence_id: int,
    residence_dto: ResidenceCreateUpdateSchema,
) -> ResidenceSchema:
    try:
        async with database.session() as session:
            updated_residence = await residence_repo.update_residence(
                session=session,
                residence_id=residence_id,
                residence=residence_dto,
            )
    except ResidenceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_residence


@router.delete("/delete_residence/{residence_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_residence(
    residence_id: int,
) -> None:
    try:
        async with database.session() as session:
            residence = await residence_repo.delete_residence(session=session, residence_id=residence_id)
    except ResidenceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return residence
