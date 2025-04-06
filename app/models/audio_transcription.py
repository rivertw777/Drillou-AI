from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class AudioTranscription(Base):
    __tablename__ = "audio_transcriptions"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    audio_file_path = Column(String(255), nullable=False)
    transcription = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __init__(self, client_id: int, audio_file_path: str, transcription: str):
        self.client_id = client_id
        self.audio_file_path = audio_file_path
        self.transcription = transcription
