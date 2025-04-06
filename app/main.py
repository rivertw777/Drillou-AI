from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import audio
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.include_router(
    audio.router,
    prefix=settings.API_V1_STR,
    tags=["audio"]
)
