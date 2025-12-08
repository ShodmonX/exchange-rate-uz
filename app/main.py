from fastapi import FastAPI

from contextlib import asynccontextmanager

from shared import settings
from routers import router


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
)

app.include_router(router)

@app.get("/health")
async def root():
    return {"status": "ok"}