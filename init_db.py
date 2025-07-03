from database import engine, Base, DBPhoto
from sqlalchemy.orm import Session

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = Session(bind=engine)
    
    initial_photos = [
        DBPhoto(
            url="https://picsum.photos/id/1/300",
            title="Photo 1",
            category="Nature",
            tags=["fleurs", "printemps"]
        ),
        DBPhoto(
            url="https://picsum.photos/id/2/300",
            title="Photo 2",
            category="Ville",  # Correction: "Ville" au lieu de "Ville"
            tags=["nuit", "lumière"]
        )
    ]
    
    if db.query(DBPhoto).count() == 0:
        db.add_all(initial_photos)
        db.commit()

if __name__ == "__main__":
    init_db()