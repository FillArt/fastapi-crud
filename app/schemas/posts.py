from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.category import CategoryOut


class PostBase(BaseModel):
    title: str
    description: str
    categories: Optional[List[int]] = None


class PostCreate(PostBase):
    author_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Заголовок поста",
                "description": "Описание поста",
                "categories": [1, 2],
                "author_id": 1,
            }
        }
    )


class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[List[int]] = None
    image_path: Optional[str] = None
    author_id: Optional[int] = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Заголовок поста",
                "description": "Описание поста",
                "categories": [1, 2],
                "author_id": 1,
                "image_path": "/path/to/image.jpg"
            }
        }
    )


class PostContentStatus(BaseModel):
    is_published: bool

class PostOut(PostBase):
    id: int
    image_path: Optional[str] = None
    is_published: bool
    created_at: datetime
    categories: List[CategoryOut]
    author_id: int

    model_config = ConfigDict(from_attributes=True)
