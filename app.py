from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
from model import Photo, PhotoCreate
from database import SessionLocal, DBPhoto
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db: SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/photos", response_model=List[Photo])
def get_photos(category: Optional[str] = None, tags: Optional[List[str]] = Query(None), db: Session = Depends(get_db)) :
    
    query = db.query(DBPhoto)

    if category:
        query = query.filter(DBPhoto.category.ilike(category))

    if tags:
        query = query.filter(DBPhoto.tags.contains(tags))
        
    return query.all()


@app.post("/photos", response_model=Photo)
def add_photo(photo_data: PhotoCreate, db: Session = Depends(get_db)):
    db_photo = DBPhoto(**photo_data.dict())
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    return new_photo

@app.delete("/photos/{photo_id}", response_model=Photo)
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = db.query(DBPhoto).filter(DBPhoto.id == photo_id).first()
    if not db_photo:
        raise HTTPException(status_code=404, detail="Photo non trouvée")
    
    db.delete(db_photo)
    db.commit()
    return db_photo
