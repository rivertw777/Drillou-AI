import os
import shutil
from fastapi import UploadFile


def save_upload_file(upload_file: UploadFile) -> str:
    # 폴더 생성
    app_dir = os.path.dirname(os.path.dirname(__file__))
    audio_dir = os.path.join(app_dir, "downloads/audio")
    os.makedirs(audio_dir, exist_ok=True)

    audio_file_path = os.path.join(audio_dir, upload_file.filename)

    with open(audio_file_path, "wb") as audio_file:
        shutil.copyfileobj(upload_file.file, audio_file)

    return audio_file_path
