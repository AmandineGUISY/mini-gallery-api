from database import engine, Base, DBPhoto
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

db = Session(bind=engine)

initial_photos = [
    DBPhoto(
        id=1,
        url="https://picsum.photos/id/1/300",
        title="Photo 1",
        category="Nature",
        tags=["fleurs", "printemps"]
    ),
    DBPhoto(
        id=2,
        url="https://picsum.photos/id/2/300",
        title="Photo 2",
        category="Ville",
        tags=["nuit", "lumière"]
    )
]

for photo in initial_photos:
    if not db.query(DBPhoto).filter(DBPhoto.id == photo.id).first():
        db.add(photo)

db.commit()