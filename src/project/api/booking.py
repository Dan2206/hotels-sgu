from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema
from project.schemas.booking import BookingSchema, BookingCreateUpdateSchema
from project.core.exceptions.booking import BookingNotFound, BookingBadForeignKey, BookingBadDate
from project.api.depends import database, booking_repo, get_current_user, check_for_admin_access

router = APIRouter()


@router.get(
    "/all_bookings",
    response_model=list[BookingSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_all_bookings() -> list[BookingSchema]:
    async with database.session() as session:
        all_bookings = await booking_repo.get_all_bookings(session=session)

    return all_bookings


@router.get(
    "/booking/{booking_id}",
    response_model=BookingSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_booking_by_id(
    booking_id: int,
) -> BookingSchema:
    try:
        async with database.session() as session:
            booking = await booking_repo.get_booking_by_id(session=session, booking_id=booking_id)
    except BookingNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return booking


@router.post(
    "/add_booking",
    response_model=BookingSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def add_booking(
    booking_dto: BookingCreateUpdateSchema,
) -> BookingSchema:
    try:
        async with database.session() as session:
            new_booking = await booking_repo.create_booking(session=session, booking=booking_dto)
    except (BookingBadForeignKey, BookingBadDate) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    return new_booking


@router.put(
    "/update_booking/{booking_id}",
    response_model=BookingSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def update_booking(
    booking_id: int,
    booking_dto: BookingCreateUpdateSchema,
) -> BookingSchema:
    try:
        async with database.session() as session:
            updated_booking = await booking_repo.update_booking(
                session=session,
                booking_id=booking_id,
                booking=booking_dto,
            )
    except BookingNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_booking


@router.delete("/delete_booking/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    check_for_admin_access(current_user)
    try:
        async with database.session() as session:
            booking = await booking_repo.delete_booking(session=session, booking_id=booking_id)
    except BookingNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return booking
