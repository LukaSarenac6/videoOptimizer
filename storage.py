import os
from fastapi import UploadFile
import shutil

UPLOAD_DIR = "videos"

def save_video(file: UploadFile, sub_category: str, category: str):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, category, sub_category, file.filename)
    os.makedirs(file_path)
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except IOError as e:
        print(f"Error saving file: {e}")
