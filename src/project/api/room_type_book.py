from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema
from project.schemas.room_type_book import RoomTypeBookSchema, RoomTypeBookCreateUpdateSchema
from project.core.exceptions.room_type_book import RoomTypeBookNotFound
from project.api.depends import database, room_type_book_repo, get_current_user, check_for_admin_access

router = APIRouter()


@router.get(
    "/all_room_type_books",
    response_model=list[RoomTypeBookSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_all_room_type_books() -> list[RoomTypeBookSchema]:
    async with database.session() as session:
        all_room_type_books = await room_type_book_repo.get_all_room_type_books(session=session)

    return all_room_type_books


@router.get(
    "/room_type_book/{room_type_book_id}",
    response_model=RoomTypeBookSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_room_type_book_by_id(
    room_type_book_id: int,
) -> RoomTypeBookSchema:
    try:
        async with database.session() as session:
            room_type_book = await room_type_book_repo.get_room_type_book_by_id(session=session, room_type_book_id=room_type_book_id)
    except RoomTypeBookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return room_type_book


@router.post("/add_room_type_book", response_model=RoomTypeBookSchema, status_code=status.HTTP_201_CREATED)
async def add_room_type_book(
    room_type_book_dto: RoomTypeBookCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> RoomTypeBookSchema:
    check_for_admin_access(user=current_user)
    async with database.session() as session:
        new_room_type_book = await room_type_book_repo.create_room_type_book(session=session, room_type_book=room_type_book_dto)
    return new_room_type_book


@router.put(
    "/update_room_type_book/{room_type_book_id}",
    response_model=RoomTypeBookSchema,
    status_code=status.HTTP_200_OK,
)
async def update_room_type_book(
    room_type_book_id: int,
    room_type_book_dto: RoomTypeBookCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> RoomTypeBookSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_room_type_book = await room_type_book_repo.update_room_type_book(
                session=session,
                room_type_book_id=room_type_book_id,
                room_type_book=room_type_book_dto,
            )
    except RoomTypeBookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_room_type_book


@router.delete("/delete_room_type_book/{room_type_book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_type_book(
    room_type_book_id: int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            room_type_book = await room_type_book_repo.delete_room_type_book(session=session, room_type_book_id=room_type_book_id)
    except RoomTypeBookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return room_type_book
