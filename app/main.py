from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.projects import router as projects_router
from app.api.tasks import router as tasks_router


app = FastAPI(title="Workspace API")

app.include_router(users_router)
app.include_router(projects_router)
app.include_router(tasks_router)