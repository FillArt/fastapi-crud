from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime

from app.schemas.category import CategoryOut


class PostBase(BaseModel):
    title: str
    description: str
    content: str
    category_ids: List[int] = []
    image_path: Optional[str] = None


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    id: int
    title: str
    description: str
    content: str
    categories: List[CategoryOut]
    image_path: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True