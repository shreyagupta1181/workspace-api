from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "todo"
    project_id: int


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    project_id: int | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    project_id: int

    model_config = {
        "from_attributes": True
    }