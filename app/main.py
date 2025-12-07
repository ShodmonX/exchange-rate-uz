from fastapi import FastAPI

from contextlib import asynccontextmanager

from shared import settings
from routers import router
from utils import start_scheduler, refresh_reference_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan
)

app.include_router(router)

@app.post("/refresh_reference_cache")
async def refresh_reference():
    await refresh_reference_cache()
    return {"status": "ok"}

@app.get("/health")
async def root():
    return {"status": "ok"}