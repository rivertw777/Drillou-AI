from sqlalchemy.orm import Session
from app.models.audio_transcription import AudioTranscription


class AudioTranscriptionRepository:
    @staticmethod
    def save(db: Session, model: AudioTranscription) -> AudioTranscription:
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    @staticmethod
    def get_by_id(db: Session, transcription_id: int) -> AudioTranscription:
        return db.query(AudioTranscription).filter(AudioTranscription.id == transcription_id).first()