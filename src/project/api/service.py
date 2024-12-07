from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema
from project.schemas.service import ServiceSchema, ServiceCreateUpdateSchema
from project.core.exceptions.serivce import ServiceNotFound, ServiceNoHotel, ServiceAlreadyExists
from project.api.depends import database, service_repo, get_current_user, check_for_admin_access

router = APIRouter()


@router.get(
    "/all_services",
    response_model=list[ServiceSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_all_services() -> list[ServiceSchema]:
    async with database.session() as session:
        all_services = await service_repo.get_all_services(session=session)

    return all_services


@router.get(
    "/service/{service_id}",
    response_model=ServiceSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_service_by_id(
    service_id: int,
) -> ServiceSchema:
    try:
        async with database.session() as session:
            service = await service_repo.get_service_by_id(session=session, service_id=service_id)
    except ServiceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return service


@router.post(
    "/add_service",
    response_model=ServiceSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_service(
    service_dto: ServiceCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> ServiceSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_service = await service_repo.create_service(session=session, service=service_dto)
    except ServiceNoHotel as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except ServiceAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_service


@router.put(
    "/update_service/{service_id}",
    response_model=ServiceSchema,
    status_code=status.HTTP_200_OK,
)
async def update_service(
    service_id: int,
    service_dto: ServiceCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> ServiceSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_service = await service_repo.update_service(
                session=session,
                service_id=service_id,
                service=service_dto,
            )
    except ServiceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_service


@router.delete(
    "/delete_service/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service(
    service_id: int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            service = await service_repo.delete_service(session=session, service_id=service_id)
    except ServiceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return service
