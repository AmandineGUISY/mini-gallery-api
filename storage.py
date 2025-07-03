import os
import uuid
from fastapi import UploadFile
from pathlib import Path
from PIL import Image
import io

UPLOAD_DIR = "static/uploads"
THUMBNAIL_DIR = "static/thumbnails"

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(THUMBNAIL_DIR).mkdir(parents=True, exist_ok=True)

async def handle_file_upload(file: UploadFile) -> dict:
    file_id = uuid.uuid4().hex # génère une id
    ext = os.path.splitext(file.filename)[1].lower()
    
    original_path = f"{UPLOAD_DIR}/{file_id}{ext}" # chemin pour les fichiers
    thumbnail_path = f"{THUMBNAIL_DIR}/{file_id}_thumb{ext}"
    
    with open(original_path, "wb") as buffer: # sauvegarde l'originale
        content = await file.read()
        buffer.write(content)
    
    img = Image.open(io.BytesIO(content))     # Creation d'une miniature
    img.thumbnail((300, 300))
    img.save(thumbnail_path)
    
    return {
        "original": f"/{original_path}",
        "thumbnail": f"/{thumbnail_path}"
    }

def delete_uploaded_files(image_url: str, thumbnail_url: str):
    try:
        if image_url and os.path.exists(image_url.lstrip('/')):
            os.remove(image_url.lstrip('/'))
        if thumbnail_url and os.path.exists(thumbnail_url.lstrip('/')):
            os.remove(thumbnail_url.lstrip('/'))
    except Exception as e:
        print(f"Erreur lors de la suppression des fichiers: {e}")