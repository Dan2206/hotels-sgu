from fastapi import APIRouter, HTTPException, status

from project.schemas.healthcheck import HealthCheckSchema
from project.api.depends import database, client_repo

router = APIRouter()


@router.get("/healthcheck", response_model=HealthCheckSchema, status_code=status.HTTP_200_OK)
async def check_health() -> HealthCheckSchema:
    async with database.session() as session:
        db_is_ok = await client_repo.check_connection(session=session)
    return HealthCheckSchema(
        db_is_ok=db_is_ok,
    )