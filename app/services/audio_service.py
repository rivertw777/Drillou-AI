from app.core.config import settings
import os
import math
import requests
from pydub import AudioSegment
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.audio_transcription import AudioTranscription
from app.repositories.audio_transcription import AudioTranscriptionRepository


class AudioService:
    def __init__(self, db: Session):
        self.db = db
        self.api_key = settings.OPENAI_API_KEY

        # 폴더 생성
        app_dir = os.path.dirname(os.path.dirname(__file__))
        self.chunks_dir = os.path.join(app_dir, "downloads/audio/chunks")
        os.makedirs(self.chunks_dir, exist_ok=True)

    """
        음성 파일을 청크로 나누고 텍스트로 변환, 저장
    """
    def convert_audio_to_text(self, audio_file_path: str, filename: str, client_id: int) -> str:
        chunk_file_paths = self._cut_audio_in_chunks(audio_file_path, filename)
        try:
            transcription = self._transcribe_chunks(chunk_file_paths)

            transcription_model = AudioTranscription(client_id=client_id, audio_file_path=audio_file_path, transcription=transcription)

            AudioTranscriptionRepository.save(self.db, transcription_model)

            return transcription
        finally:
            self.cleanup_files(audio_file_path, chunk_file_paths)

    def _cut_audio_in_chunks(self, audio_file_path: str, filename: str) -> list:
        track = AudioSegment.from_file(audio_file_path)

        # Define chunk size as 1 minute
        chunk_len = 1 * 60 * 1000

        # Calculate total number of chunks
        chunks = math.ceil(len(track) / chunk_len)
        chunk_file_paths = []

        for i in range(chunks):
            start_time = i * chunk_len
            end_time = min((i + 1) * chunk_len, len(track))
            chunk = track[start_time:end_time]
            chunk_file_path = os.path.join(self.chunks_dir, f"{filename}_chunk_{i}.mp3")
            chunk.export(chunk_file_path, format="mp3")
            chunk_file_paths.append(chunk_file_path)

        return chunk_file_paths

    def _transcribe_chunks(self, chunk_files: list) -> str:
        final_transcript = ""

        for file in chunk_files:
            with open(file, "rb") as audio_file:
                response = requests.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    files={"file": audio_file},
                    data={"model": "whisper-1"}
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Whisper API error: {response.text}"
                    )

                transcript = response.json().get("text", "")
                final_transcript += transcript + "\n"

        return final_transcript.strip()

    @staticmethod
    def cleanup_files(audio_file_path: str, chunk_files: list) -> None:
        os.remove(audio_file_path)
        for file_path in chunk_files:
            os.remove(file_path)
