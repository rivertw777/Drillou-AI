from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from app.tasks.convert_audio_to_text import convert_audio_to_text
from app.tasks.extract_keyword_from_text import extract_keyword_from_text
from app.utils.file_handler import save_upload_file
from celery import chain

router = APIRouter()


# TODO: 음성 파일 AWS S3 관리
@router.post("/audio/process/")
def process_audio(
        client_id: int = Form(...),
        audio_file: UploadFile = File(...),
):
    try:
        # 음성 파일 저장
        audio_file_path = save_upload_file(audio_file)

        task_chain = chain(
            convert_audio_to_text.s(audio_file_path, audio_file.filename, client_id),  # 텍스트 변환
            extract_keyword_from_text.s()  # 키워드 추출
        )

        result = task_chain.apply_async()

        return {
            "message": "음성 파일이 저장되었습니다. 비동기 작업이 시작됩니다.",
            "task_id": result.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
