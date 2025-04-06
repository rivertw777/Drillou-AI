from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.audio_service import AudioService
from app.services.llm_service import LLMService
from app.utils.file_handler import save_upload_file

router = APIRouter()


# TODO: 음성 파일 AWS S3 관리
@router.post("/audio/process/")
async def process_audio(
    client_id: int,
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        # 음성 파일 저장
        audio_file_path = await save_upload_file(audio_file)

        # 음성 파일 텍스트 변환
        transcription = await AudioService(db=db).process_audio_file(audio_file_path, audio_file.filename, client_id)

        # 계약 키워드 추출
        await LLMService(db=db).extract_contract_keywords(transcription, client_id)

        return {"message": "작업 완료"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
