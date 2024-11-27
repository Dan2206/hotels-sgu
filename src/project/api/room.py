from fastapi import APIRouter, HTTPException, status

from project.schemas.room import RoomSchema, RoomCreateUpdateSchema
from project.core.exceptions.room import RoomNoHotel, RoomNumAlreadyExists, RoomNotFound
from project.api.depends import database, client_repo, hotel_repo, room_repo

router = APIRouter()


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
