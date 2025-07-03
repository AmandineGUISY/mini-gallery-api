from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from database import SessionLocal, DBPhoto
from schemas import Photo
from sqlalchemy.orm import Session
from storage import handle_file_upload, delete_uploaded_files

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            query = query.filter(DBPhoto.tags.contains(tag))
        
    return query.all()

@app.post("/photos", response_model=Photo)
async def create_photo(
    title: str = Form(...),
    category: Optional[str] = Form(None),
    tags: Optional[List[str]] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    urls = await handle_file_upload(file)

    db_photo = DBPhoto(
        title=title,
        category=category,
        tags=tags or [],
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
    
    delete_uploaded_files(db_photo.image_url, db_photo.thumbnail_url)

    db.delete(db_photo)
    db.commit()
    return db_photo
