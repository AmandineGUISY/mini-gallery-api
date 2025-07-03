from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    title = Column(String)
    category = Column(String, index=True)
    tags = Column(JSON)