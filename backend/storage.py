import os
from fastapi import UploadFile
import shutil

BASE_DIR = r"C:\Users\LukaSarenac\Documents\Luka\videoOptimizer"
UPLOAD_DIR = os.path.join(BASE_DIR, "videos")

def save_video(file: UploadFile, sub_category: str, category: str):
    dir_path = os.path.join(UPLOAD_DIR, category, sub_category)
    file_path = os.path.join(UPLOAD_DIR, category, sub_category, file.filename)
    os.makedirs(dir_path, exist_ok=True)
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except IOError as e:
        print(f"Error saving file: {e}")
