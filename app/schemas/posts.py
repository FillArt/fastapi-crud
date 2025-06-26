from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class PostBase(BaseModel):
    title: str
    description: str
    categories: Optional[List[int]] = None


class PostCreate(PostBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Заголовок поста",
                "description": "Описание поста",
                "categories": [1, 2]
            }
        }
    )


class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[List[int]] = None
    image_path: Optional[str] = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Заголовок поста",
                "description": "Описание поста",
                "categories": [1, 2],
                "image_path": "/path/to/image.jpg"
            }
        }
    )


class PostOut(PostBase):
    pk_id: int
    image_path: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
