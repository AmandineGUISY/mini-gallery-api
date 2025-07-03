from pydantic import BaseModel
from typing import List

class PhotoBase(BaseModel):
    title: str
    category: str = None
    tags: List[str] = None

class PhotoCreate(PhotoBase):
    pass

class Photo(PhotoBase):
    id: int
    image_url: str
    thumbnail_url: str

    class Config:
        from_attributes = True