from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema
from project.schemas.price_service import PriceServiceSchema, PriceServiceCreateUpdateSchema
from project.core.exceptions.price import PriceNotFound, PriceBadPrice, PriceBadForeignKey, PriceBadDate
from project.api.depends import database, price_service_repo, get_current_user, check_for_admin_access

router = APIRouter()


@router.get(
    "/all_price_services",
    response_model=list[PriceServiceSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_all_price_services() -> list[PriceServiceSchema]:
    async with database.session() as session:
        all_price_services = await price_service_repo.get_all_price_services(session=session)

    return all_price_services


@router.get(
    "/price_service/{price_service_id}",
    response_model=PriceServiceSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_price_service_by_id(
    price_service_id: int,
) -> PriceServiceSchema:
    try:
        async with database.session() as session:
            price_service = await price_service_repo.get_price_service_by_id(session=session, price_service_id=price_service_id)
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return price_service


@router.post("/add_price_service", response_model=PriceServiceSchema, status_code=status.HTTP_201_CREATED)
async def add_price_service(
    price_service_dto: PriceServiceCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> PriceServiceSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_price_service = await price_service_repo.create_price_service(session=session, price_service=price_service_dto)
    except (PriceBadDate, PriceBadForeignKey, PriceBadPrice) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    return new_price_service


@router.put(
    "/update_price_service/{price_service_id}",
    response_model=PriceServiceSchema,
    status_code=status.HTTP_200_OK,
)
async def update_price_service(
    price_service_id: int,
    price_service_dto: PriceServiceCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> PriceServiceSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_price_service = await price_service_repo.update_price_service(
                session=session,
                price_service_id=price_service_id,
                price_service=price_service_dto,
            )
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_price_service


@router.delete("/delete_price_service/{price_service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_price_service(
    price_service_id: int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            price_service = await price_service_repo.delete_price_service(session=session, price_service_id=price_service_id)
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return price_service
