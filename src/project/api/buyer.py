from fastapi import APIRouter, HTTPException, status

from project.schemas.buyer import BuyerSchema, BuyerCreateUpdateSchema
from project.core.exceptions.buyer import BuyerNotFound
from project.api.depends import database, buyer_repo

router = APIRouter()


@router.get("/all_buyers", response_model=list[BuyerSchema], status_code=status.HTTP_200_OK)
async def get_all_buyers() -> list[BuyerSchema]:
    async with database.session() as session:
        all_buyers = await buyer_repo.get_all_buyers(session=session)

    return all_buyers


@router.get("/buyer/{buyer_id}", response_model=BuyerSchema, status_code=status.HTTP_200_OK)
async def get_buyer_by_id(
    buyer_id: int,
) -> BuyerSchema:
    try:
        async with database.session() as session:
            buyer = await buyer_repo.get_buyer_by_id(session=session, buyer_id=buyer_id)
    except BuyerNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return buyer


@router.post("/add_buyer", response_model=BuyerSchema, status_code=status.HTTP_201_CREATED)
async def add_buyer(
    buyer_dto: BuyerCreateUpdateSchema,
) -> BuyerSchema:
    async with database.session() as session:
        new_buyer = await buyer_repo.create_buyer(session=session, buyer=buyer_dto)
    return new_buyer


@router.put(
    "/update_buyer/{buyer_id}",
    response_model=BuyerSchema,
    status_code=status.HTTP_200_OK,
)
async def update_buyer(
    buyer_id: int,
    buyer_dto: BuyerCreateUpdateSchema,
) -> BuyerSchema:
    try:
        async with database.session() as session:
            updated_buyer = await buyer_repo.update_buyer(
                session=session,
                buyer_id=buyer_id,
                buyer=buyer_dto,
            )
    except BuyerNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_buyer


@router.delete("/delete_buyer/{buyer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_buyer(
    buyer_id: int,
) -> None:
    try:
        async with database.session() as session:
            buyer = await buyer_repo.delete_buyer(session=session, buyer_id=buyer_id)
    except BuyerNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return buyer
