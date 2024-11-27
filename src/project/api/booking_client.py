from fastapi import APIRouter, HTTPException, status

from project.schemas.booking_client import BookingClientSchema, BookingClientCreateUpdateSchema
from project.core.exceptions.booking_client import BookingClientNotFound
from project.api.depends import database, booking_client_repo

router = APIRouter()


@router.get("/all_booking_clients", response_model=list[BookingClientSchema], status_code=status.HTTP_200_OK)
async def get_all_booking_clients() -> list[BookingClientSchema]:
    async with database.session() as session:
        all_booking_clients = await booking_client_repo.get_all_booking_clients(session=session)

    return all_booking_clients


@router.get("/booking_client/{booking_client_id}", response_model=BookingClientSchema, status_code=status.HTTP_200_OK)
async def get_booking_client_by_id(
    booking_client_id: int,
) -> BookingClientSchema:
    try:
        async with database.session() as session:
            booking_client = await booking_client_repo.get_booking_client_by_id(session=session, booking_client_id=booking_client_id)
    except BookingClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return booking_client


@router.post("/add_booking_client", response_model=BookingClientSchema, status_code=status.HTTP_201_CREATED)
async def add_booking_client(
    booking_client_dto: BookingClientCreateUpdateSchema,
) -> BookingClientSchema:
    async with database.session() as session:
        new_booking_client = await booking_client_repo.create_booking_client(session=session, booking_client=booking_client_dto)
    return new_booking_client


@router.put(
    "/update_booking_client/{booking_client_id}",
    response_model=BookingClientSchema,
    status_code=status.HTTP_200_OK,
)
async def update_booking_client(
    booking_client_id: int,
    booking_client_dto: BookingClientCreateUpdateSchema,
) -> BookingClientSchema:
    try:
        async with database.session() as session:
            updated_booking_client = await booking_client_repo.update_booking_client(
                session=session,
                booking_client_id=booking_client_id,
                booking_client=booking_client_dto,
            )
    except BookingClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_booking_client


@router.delete("/delete_booking_client/{booking_client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking_client(
    booking_client_id: int,
) -> None:
    try:
        async with database.session() as session:
            booking_client = await booking_client_repo.delete_booking_client(session=session, booking_client_id=booking_client_id)
    except BookingClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return booking_client
