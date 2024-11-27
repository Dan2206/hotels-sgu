from fastapi import APIRouter, HTTPException, status

from project.schemas.healthcheck import HealthCheckSchema
from project.schemas.client import ClientSchema, ClientCreateUpdateSchema
from project.schemas.hotel import HotelSchema, HotelCreateUpdateSchema
from project.schemas.room import RoomSchema, RoomCreateUpdateSchema
from project.schemas.room_type_book import RoomTypeBookSchema, RoomTypeBookCreateUpdateSchema
from project.schemas.room_type import RoomTypeSchema, RoomTypeCreateUpdateSchema
from project.schemas.price import PriceSchema, PriceCreateUpdateSchema
from project.schemas.buyer import BuyerSchema, BuyerCreateUpdateSchema
from project.schemas.booking import BookingSchema, BookingCreateUpdateSchema
from project.schemas.booking_client import BookingClientSchema, BookingClientCreateUpdateSchema
from project.schemas.residence import ResidenceSchema, ResidenceCreateUpdateSchema
from project.schemas.residence_client import ResidenceClientSchema, ResidenceClientCreateUpdateSchema
from project.schemas.service import ServiceSchema, ServiceCreateUpdateSchema
from project.schemas.service_rendered import ServiceRenderedSchema, ServiceRenderedCreateUpdateSchema
from project.schemas.price_service import PriceServiceSchema, PriceServiceCreateUpdateSchema

from project.core.exceptions import ClientNotFound, ClientAlreadyExists, ClientAlreadyExistsEmail, ClientAlreadyExistsDoc
from project.core.exceptions import HotelNotFound, HotelStarsIncorrect, HotelAlreadyExists
from project.core.exceptions import RoomNoHotel, RoomNumAlreadyExists, RoomNotFound
from project.core.exceptions import BuyerNotFound
from project.core.exceptions import BookingNotFound, BookingBadForeignKey, BookingBadDate
from project.core.exceptions import BookingClientNotFound
# price exceptions are common for prices of rooms and prices of services
from project.core.exceptions import PriceNotFound, PriceBadForeignKey, PriceBadDate, PriceBadPrice
from project.core.exceptions import ResidenceClientNotFound
from project.core.exceptions import ResidenceNotFound, ResidenceBadForeignKey, ResidenceBadDate
from project.core.exceptions import RoomTypeBookNotFound
from project.core.exceptions import RoomTypeNotFound, RoomTypeBadForeignKey, RoomTypeBadDate
from project.core.exceptions import ServiceRenderedNotFound, ServiceRenderedBadForeignKey
from project.core.exceptions import ServiceAlreadyExists, ServiceNoHotel, ServiceNotFound

from project.api.depends import database, client_repo, hotel_repo, room_repo

router = APIRouter()


# ========== HEALTHCHECK ==========


@router.get("/healthcheck", response_model=HealthCheckSchema, status_code=status.HTTP_200_OK)
async def check_health() -> HealthCheckSchema:
    async with database.session() as session:
        db_is_ok = await client_repo.check_connection(session=session)
    return HealthCheckSchema(
        db_is_ok=db_is_ok,
    )


# ========== CLIENTS ==========


@router.get("/all_clients", response_model=list[ClientSchema], status_code=status.HTTP_200_OK)
async def get_all_clients() -> list[ClientSchema]:
    async with database.session() as session:
        all_clients = await client_repo.get_all_clients(session=session)

    return all_clients


@router.get("/client/{client_id}", response_model=ClientSchema, status_code=status.HTTP_200_OK)
async def get_client_by_id(
    client_id: int,
) -> ClientSchema:
    try:
        async with database.session() as session:
            client = await client_repo.get_client_by_id(session=session, client_id=client_id)
    except ClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return client


@router.post("/add_client", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
async def add_client(
    client_dto: ClientCreateUpdateSchema,
) -> ClientSchema:
    try:
        async with database.session() as session:
            new_client = await client_repo.create_client(session=session, client=client_dto)
    except (ClientAlreadyExists, ClientAlreadyExistsEmail, ClientAlreadyExistsDoc) as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_client


@router.put(
    "/update_client/{client_id}",
    response_model=ClientSchema,
    status_code=status.HTTP_200_OK,
)
async def update_client(
    client_id: int,
    client_dto: ClientCreateUpdateSchema,
) -> ClientSchema:
    try:
        async with database.session() as session:
            updated_client = await client_repo.update_client(
                session=session,
                client_id=client_id,
                client=client_dto,
            )
    except ClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_client


@router.delete("/delete_client/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
) -> None:
    try:
        async with database.session() as session:
            client = await client_repo.delete_client(session=session, client_id=client_id)
    except ClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return client


# ========== HOTELS ==========


@router.get("/all_hotels", response_model=list[HotelSchema], status_code=status.HTTP_200_OK)
async def get_all_hotels() -> list[HotelSchema]:
    async with database.session() as session:
        all_hotels = await hotel_repo.get_all_hotels(session=session)

    return all_hotels


@router.get("/hotel/{hotel_id}", response_model=HotelSchema, status_code=status.HTTP_200_OK)
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
) -> HotelSchema:
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
) -> HotelSchema:
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
) -> None:
    try:
        async with database.session() as session:
            hotel = await hotel_repo.delete_hotel(session=session, hotel_id=hotel_id)
    except HotelNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return hotel


# ========== ROOMS ==========


@router.get("/all_rooms", response_model=list[RoomSchema], status_code=status.HTTP_200_OK)
async def get_all_rooms() -> list[RoomSchema]:
    async with database.session() as session:
        all_rooms = await room_repo.get_all_rooms(session=session)

    return all_rooms


@router.get("/room/{room_id}", response_model=RoomSchema, status_code=status.HTTP_200_OK)
async def get_room_by_id(
    room_id: int,
) -> RoomSchema:
    try:
        async with database.session() as session:
            room = await room_repo.get_room_by_id(session=session, room_id=room_id)
    except RoomNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return room


@router.post("/add_room", response_model=RoomSchema, status_code=status.HTTP_201_CREATED)
async def add_room(
    room_dto: RoomCreateUpdateSchema,
) -> RoomSchema:
    try:
        async with database.session() as session:
            new_room = await room_repo.create_room(session=session, room=room_dto)
    except RoomNumAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except RoomNoHotel as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    return new_room


@router.put(
    "/update_room/{room_id}",
    response_model=RoomSchema,
    status_code=status.HTTP_200_OK,
)
async def update_room(
    room_id: int,
    room_dto: RoomCreateUpdateSchema,
) -> RoomSchema:
    try:
        async with database.session() as session:
            updated_room = await room_repo.update_room(
                session=session,
                room_id=room_id,
                room=room_dto,
            )
    except RoomNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_room


@router.delete("/delete_room/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: int,
) -> None:
    try:
        async with database.session() as session:
            room = await room_repo.delete_room(session=session, room_id=room_id)
    except RoomNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return room