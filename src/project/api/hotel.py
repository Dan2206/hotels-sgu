from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema
from project.schemas.hotel import HotelSchema, HotelCreateUpdateSchema
from project.core.exceptions.hotel import HotelNotFound, HotelStarsIncorrect, HotelAlreadyExists
from project.api.depends import database, hotel_repo, get_current_user, check_for_admin_access

router = APIRouter()


@router.get(
    "/all_hotels",
    response_model=list[HotelSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_all_hotels() -> list[HotelSchema]:
    async with database.session() as session:
        all_hotels = await hotel_repo.get_all_hotels(session=session)

    return all_hotels


@router.get(
    "/hotel/{hotel_id}",
    response_model=HotelSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_hotel_by_id(
    hotel_id: int,
) -> HotelSchema:
    try:
        async with database.session() as session:
            hotel = await hotel_repo.get_hotel_by_id(session=session, hotel_id=hotel_id)
    except HotelNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return hotel


@router.post("/add_hotel", response_model=HotelSchema, status_code=status.HTTP_201_CREATED)
async def add_hotel(
    hotel_dto: HotelCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> HotelSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_hotel = await hotel_repo.create_hotel(session=session, hotel=hotel_dto)
    except HotelAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except HotelStarsIncorrect as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    return new_hotel


@router.put(
    "/update_hotel/{hotel_id}",
    response_model=HotelSchema,
    status_code=status.HTTP_200_OK,
)
async def update_hotel(
    hotel_id: int,
    hotel_dto: HotelCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> HotelSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_hotel = await hotel_repo.update_hotel(
                session=session,
                hotel_id=hotel_id,
                hotel=hotel_dto,
            )
    except HotelNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_hotel


@router.delete("/delete_hotel/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(
    hotel_id: int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            hotel = await hotel_repo.delete_hotel(session=session, hotel_id=hotel_id)
    except HotelNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return hotel
