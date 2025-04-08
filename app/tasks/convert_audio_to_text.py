from app.celery_app import celery_app
from app.core.database import get_db
from app.services.audio_service import AudioService


@celery_app.task
def convert_audio_to_text(audio_file_path, filename, client_id):
    try:
        db = next(get_db())
        transcription = AudioService(db=db).convert_audio_to_text(audio_file_path, filename, client_id)

        return {
            "status": "success",
            "client_id": client_id,
            "transcription": transcription
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}