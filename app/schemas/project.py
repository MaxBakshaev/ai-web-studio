from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

TECH_STACKS = {"static", "fullstack"}


class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    prompt: str = Field(min_length=10, max_length=5000)
    tech_stack: str = Field(default="static", max_length=50)


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    prompt: str
    tech_stack: str
    status: str
    created_at: datetime
