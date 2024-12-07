from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema
from project.schemas.price import PriceSchema, PriceCreateUpdateSchema
from project.core.exceptions.price import PriceNotFound, PriceBadPrice, PriceBadForeignKey, PriceBadDate
from project.api.depends import database, price_repo, get_current_user, check_for_admin_access

router = APIRouter()


@router.get(
    "/all_prices",
    response_model=list[PriceSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_all_prices() -> list[PriceSchema]:
    async with database.session() as session:
        all_prices = await price_repo.get_all_prices(session=session)

    return all_prices


@router.get(
    "/price/{price_id}",
    response_model=PriceSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_price_by_id(
    price_id: int,
) -> PriceSchema:
    try:
        async with database.session() as session:
            price = await price_repo.get_price_by_id(session=session, price_id=price_id)
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return price


@router.post("/add_price", response_model=PriceSchema, status_code=status.HTTP_201_CREATED)
async def add_price(
    price_dto: PriceCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> PriceSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_price = await price_repo.create_price(session=session, price=price_dto)
    except (PriceBadDate, PriceBadPrice, PriceBadForeignKey) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    return new_price


@router.put(
    "/update_price/{price_id}",
    response_model=PriceSchema,
    status_code=status.HTTP_200_OK,
)
async def update_price(
    price_id: int,
    price_dto: PriceCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> PriceSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_price = await price_repo.update_price(
                session=session,
                price_id=price_id,
                price=price_dto,
            )
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_price


@router.delete("/delete_price/{price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_price(
    price_id: int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            price = await price_repo.delete_price(session=session, price_id=price_id)
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return price
