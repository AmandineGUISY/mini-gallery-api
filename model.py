from pydantic import BaseModel
from typing import List, Optional

class Photo(BaseModel):
    id: int
    url: str
    title: str
    category: str
    tags: List[str]