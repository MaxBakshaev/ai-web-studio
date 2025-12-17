from datetime import datetime
from pydantic import BaseModel, ConfigDict


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    status: str
    error_message: str | None
    created_at: datetime
    finished_at: datetime | None
