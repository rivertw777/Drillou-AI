from app.celery_app import celery_app
from app.core.database import get_db
from app.services.llm_service import LLMService


@celery_app.task
def extract_keyword_from_text(task_result):
    if task_result.get("status") != "success":
        return task_result

    client_id = task_result.get("client_id")
    transcription = task_result.get("transcription")

    try:
        db = next(get_db())
        keywords = LLMService(db=db).extract_contract_keywords(transcription, client_id)

        return {
            "status": "success",
            "client_id": client_id,
            "keywords": keywords
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
