from pydantic import BaseModel
class HealthCheckSchema(BaseModel):
    db_is_ok: bool