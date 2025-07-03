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