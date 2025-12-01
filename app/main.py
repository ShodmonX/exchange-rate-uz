from fastapi import FastAPI

from shared import settings

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION
)

@app.get("/health")
async def root():
    return {"status": "ok"}