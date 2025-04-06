import os
import shutil
from fastapi import UploadFile


async def save_upload_file(upload_file: UploadFile) -> str:
    audio_dir = "../audio"
    os.makedirs(audio_dir, exist_ok=True)

    audio_file_path = os.path.join(audio_dir, upload_file.filename)

    with open(audio_file_path, "wb") as audio_file:
        shutil.copyfileobj(upload_file.file, audio_file)

    return audio_file_path
