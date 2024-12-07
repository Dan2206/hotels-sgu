from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema
from project.schemas.residence_client import ResidenceClientSchema, ResidenceClientCreateUpdateSchema
from project.core.exceptions.residence_client import ResidenceClientNotFound
from project.api.depends import database, residence_client_repo, get_current_user, check_for_admin_access

router = APIRouter()


@router.get(
    "/all_residence_clients",
    response_model=list[ResidenceClientSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_all_residence_clients() -> list[ResidenceClientSchema]:
    async with database.session() as session:
        all_residence_clients = await residence_client_repo.get_all_residence_clients(session=session)

    return all_residence_clients


@router.get(
    "/residence_client/{residence_client_id}",
    response_model=ResidenceClientSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_residence_client_by_id(
    residence_client_id: int,
) -> ResidenceClientSchema:
    try:
        async with database.session() as session:
            residence_client = await residence_client_repo.get_residence_client_by_id(session=session, residence_client_id=residence_client_id)
    except ResidenceClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return residence_client


@router.post(
    "/add_residence_client",
    response_model=ResidenceClientSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def add_residence_client(
    residence_client_dto: ResidenceClientCreateUpdateSchema,
) -> ResidenceClientSchema:
    async with database.session() as session:
        new_residence_client = await residence_client_repo.create_residence_client(session=session, residence_client=residence_client_dto)
    return new_residence_client


@router.put(
    "/update_residence_client/{residence_client_id}",
    response_model=ResidenceClientSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def update_residence_client(
    residence_client_id: int,
    residence_client_dto: ResidenceClientCreateUpdateSchema,
) -> ResidenceClientSchema:
    try:
        async with database.session() as session:
            updated_residence_client = await residence_client_repo.update_residence_client(
                session=session,
                residence_client_id=residence_client_id,
                residence_client=residence_client_dto,
            )
    except ResidenceClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_residence_client


@router.delete("/delete_residence_client/{residence_client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_residence_client(
    residence_client_id: int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            residence_client = await residence_client_repo.delete_residence_client(session=session, residence_client_id=residence_client_id)
    except ResidenceClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return residence_client
