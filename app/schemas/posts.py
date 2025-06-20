from typing import List

from pydantic import BaseModel

from app.schemas.category import CategoryOut


class PostBase(BaseModel):
    title: str
    description: str
    content: str
    category_ids: List[int] = []
    image_path: str


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    categories: List[CategoryOut]
    image_path: str

    class Config:
        orm_mode = True