import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.users import router as users_router
from app.api.projects import router as projects_router
from app.api.tasks import router as tasks_router
from app.api.auth import router as auth_router
from app.api.oauth import router as oauth_router

load_dotenv()

app = FastAPI(title="Workspace API")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
)

app.include_router(users_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(oauth_router)