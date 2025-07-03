from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query
from typing import List, Optional
from database import SessionLocal, DBPhoto
from schemas import Photo
from sqlalchemy.orm import Session
from storage import handle_file_upload

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/photos/{photo_id}", response_model=Photo)
def read_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = db.query(DBPhoto).filter(DBPhoto.id == photo_id).first()
    if not db_photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return db_photo

@app.get("/photos", response_model=List[Photo])
def get_photos(category: Optional[str] = None, tags: Optional[List[str]] = Query(None), db: Session = Depends(get_db)) :
    
    query = db.query(DBPhoto)

    if category:
        query = query.filter(DBPhoto.category.ilike(f"%{category}%"))

    if tags:
        for tag in tags:
            query = query.filter(DBPhoto.tags.contains([tag]))
        
    return query.all()

@app.post("/photos", response_model=Photo)
async def create_photo(
    title: str = Form(...),
    category: str = Form(...),
    tags: List[str] = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    urls = await handle_file_upload(file)

    db_photo = DBPhoto(
        title=title,
        category=category,
        tags=tags,
        image_url=urls["original"],
        thumbnail_url=urls["thumbnail"]
    )

    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    return db_photo

@app.delete("/photos/{photo_id}", response_model=Photo)
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = db.query(DBPhoto).filter(DBPhoto.id == photo_id).first()
    if not db_photo:
        raise HTTPException(status_code=404, detail="Photo non trouvée")
    
    db.delete(db_photo)
    db.commit()
    return db_photo
