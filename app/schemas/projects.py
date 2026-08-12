from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    owner_id: int


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    owner_id: int | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int

    model_config = {
        "from_attributes": True
    }