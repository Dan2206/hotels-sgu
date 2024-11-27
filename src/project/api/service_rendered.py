from fastapi import APIRouter, HTTPException, status

from project.schemas.service_rendered import ServiceRenderedSchema, ServiceRenderedCreateUpdateSchema
from project.core.exceptions.service_rendered import ServiceRenderedNotFound, ServiceRenderedBadForeignKey
from project.api.depends import database, service_rendered_repo

router = APIRouter()


@router.get("/all_service_rendereds", response_model=list[ServiceRenderedSchema], status_code=status.HTTP_200_OK)
async def get_all_service_rendereds() -> list[ServiceRenderedSchema]:
    async with database.session() as session:
        all_service_rendereds = await service_rendered_repo.get_all_service_rendereds(session=session)

    return all_service_rendereds


@router.get("/service_rendered/{service_rendered_id}", response_model=ServiceRenderedSchema, status_code=status.HTTP_200_OK)
async def get_service_rendered_by_id(
    service_rendered_id: int,
) -> ServiceRenderedSchema:
    try:
        async with database.session() as session:
            service_rendered = await service_rendered_repo.get_service_rendered_by_id(session=session, service_rendered_id=service_rendered_id)
    except ServiceRenderedNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return service_rendered


@router.post("/add_service_rendered", response_model=ServiceRenderedSchema, status_code=status.HTTP_201_CREATED)
async def add_service_rendered(
    service_rendered_dto: ServiceRenderedCreateUpdateSchema,
) -> ServiceRenderedSchema:
    try:
        async with database.session() as session:
            new_service_rendered = await service_rendered_repo.create_service_rendered(session=session, service_rendered=service_rendered_dto)
    except ServiceRenderedBadForeignKey as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    return new_service_rendered


@router.put(
    "/update_service_rendered/{service_rendered_id}",
    response_model=ServiceRenderedSchema,
    status_code=status.HTTP_200_OK,
)
async def update_service_rendered(
    service_rendered_id: int,
    service_rendered_dto: ServiceRenderedCreateUpdateSchema,
) -> ServiceRenderedSchema:
    try:
        async with database.session() as session:
            updated_service_rendered = await service_rendered_repo.update_service_rendered(
                session=session,
                service_rendered_id=service_rendered_id,
                service_rendered=service_rendered_dto,
            )
    except ServiceRenderedNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_service_rendered


@router.delete("/delete_service_rendered/{service_rendered_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_rendered(
    service_rendered_id: int,
) -> None:
    try:
        async with database.session() as session:
            service_rendered = await service_rendered_repo.delete_service_rendered(session=session, service_rendered_id=service_rendered_id)
    except ServiceRenderedNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return service_rendered
