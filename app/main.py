from fastapi import FastAPI

from app.api.users import router as users_router


app = FastAPI(title="Workspace API")

app.include_router(users_router)