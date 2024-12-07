from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema
from project.schemas.room_type import RoomTypeSchema, RoomTypeCreateUpdateSchema
from project.core.exceptions.room_type import RoomTypeNotFound, RoomTypeBadForeignKey, RoomTypeBadDate
from project.api.depends import database, room_type_repo, get_current_user, check_for_admin_access

router = APIRouter()


@router.get(
    "/all_room_types",
    response_model=list[RoomTypeSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_all_room_types() -> list[RoomTypeSchema]:
    async with database.session() as session:
        all_room_types = await room_type_repo.get_all_room_types(session=session)

    return all_room_types


@router.get(
    "/room_type/{room_type_id}",
    response_model=RoomTypeSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_room_type_by_id(
    room_type_id: int,
) -> RoomTypeSchema:
    try:
        async with database.session() as session:
            room_type = await room_type_repo.get_room_type_by_id(session=session, room_type_id=room_type_id)
    except RoomTypeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return room_type


@router.post("/add_room_type", response_model=RoomTypeSchema, status_code=status.HTTP_201_CREATED)
async def add_room_type(
    room_type_dto: RoomTypeCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> RoomTypeSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_room_type = await room_type_repo.create_room_type(session=session, room_type=room_type_dto)
    except (RoomTypeBadDate, RoomTypeBadForeignKey) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    return new_room_type


@router.put(
    "/update_room_type/{room_type_id}",
    response_model=RoomTypeSchema,
    status_code=status.HTTP_200_OK,
)
async def update_room_type(
    room_type_id: int,
    room_type_dto: RoomTypeCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> RoomTypeSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_room_type = await room_type_repo.update_room_type(
                session=session,
                room_type_id=room_type_id,
                room_type=room_type_dto,
            )
    except RoomTypeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_room_type


@router.delete("/delete_room_type/{room_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_type(
    room_type_id: int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            room_type = await room_type_repo.delete_room_type(session=session, room_type_id=room_type_id)
    except RoomTypeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return room_type
