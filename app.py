from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from model import Photo
from pydantic import BaseModel

app = FastAPI()

class PhotoCreate(BaseModel):
    url:str
    title:str
    category:str
    tags:List[str]

photos_db: List[Photo] = [
    Photo(id=1, url="https://picsum.photos/id/1/300", title="Photo 1", category="Nature", tags=["fleurs", "printemps"]),
    Photo(id=2, url="https://picsum.photos/id/2/300", title="Photo 2", category="Ville", tags=["nuit", "lumière"]),
]

@app.get("/photos", response_model=List[Photo])
def get_photos(category: Optional[str] = None, tags: Optional[List[str]] = Query(None)):
    results = photos_db
    if category:
        results = [photo for photo in results if photo.category.lower() == category.lower()]
    if tags:
        results = [photo for photo in results if any(tag in photo.tags for tag in tags)]
    return results

@app.post("/photos", response_model=Photo)
def add_photo(photo_data: PhotoCreate):
    new_id = max(p.id for p in photos_db) + 1 if photos_db else 1
    new_photo = Photo(id=new_id, **photo_data.dict())

    photos_db.append(new_photo)
    return new_photo

@app.delete("/photos/{photo_id}", response_model=Photo)
def delete_photo(photo_id: int):
    for i, photo in enumerate(photos_db):
        if photo.id == photo_id:
            deleted = photos_db.pop(i)
            return deleted
    raise HTTPException(status_code=404, detail="Photo non trouvée")
