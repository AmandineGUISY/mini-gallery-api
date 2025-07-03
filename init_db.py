from database import engine, Base, DBPhoto
from sqlalchemy.orm import Session

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = Session(bind=engine)
    
    initial_photos = [
        DBPhoto(
            title="Photo 1",
            category="Nature",
            tags=["fleurs", "printemps"],
            image_url="https://picsum.photos/id/1/300",
            thumbnail_url="https://picsum.photos/id/1/150"
        ),
        DBPhoto(
            title="Photo 2",
            category="Ville",  # Correction: "Ville" au lieu de "Ville"
            tags=["nuit", "lumière"],
            image_url="https://picsum.photos/id/2/300",
            thumbnail_url="https://picsum.photos/id/2/150"
        )
    ]
    
    if db.query(DBPhoto).count() == 0:
        db.add_all(initial_photos)
        db.commit()

if __name__ == "__main__":
    init_db()