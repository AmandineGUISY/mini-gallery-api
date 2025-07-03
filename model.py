from pydantic import BaseModel
from typing import List, Optional

class PhotoBase(BaseModel):
    url: str
    title: str
    category: str
    tags: List[str]

class PhotoCreate(PhotoBase):
    pass

class Photo(PhotoBase):
    id:int

    class Config:
        orm_mode=True
        schema_extra = {
            "example": {
                "id": 1,
                "url": "https://example.com/photo.jpg",
                "title": "Une belle photo",
                "category": "Nature",
                "tags": ["paysage", "montagne"]
            }
        }