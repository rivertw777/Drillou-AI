from celery import Celery
from app.core.config import settings

celery_app = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.convert_audio_to_text",
             "app.tasks.extract_keyword_from_text"]
)