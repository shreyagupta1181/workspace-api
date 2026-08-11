from fastapi import FastAPI

app = FastAPI(
    title="Workspace API",
    description="A production-grade collaborative workspace backend built with FastAPI.",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "Workspace API is running 🚀",
    }