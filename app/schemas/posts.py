from typing import List, Optional, Union, Literal
from pydantic import BaseModel
from datetime import datetime

from app.schemas.category import CategoryOut


class TextValue(BaseModel):
    content: str


class TitleValue(BaseModel):
    title: str


class QuoteValue(BaseModel):
    content: str
    author: Optional[str] = None


class ImageValue(BaseModel):
    url: str
    title: Optional[str] = None
    text: Optional[str] = None
    alt: Optional[str] = None


ValueType = Union[TextValue, TitleValue, QuoteValue, ImageValue]


class ContentBlock(BaseModel):
    id: int
    type: Literal["text", "title", "quote", "image"]
    value: ValueType
    order: int


class PostBase(BaseModel):
    title: str
    description: str
    content_blocks: List[ContentBlock]
    category_ids: List[int] = []
    # image_path: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_blocks: Optional[List[ContentBlock]] = None
    image_path: Optional[str] = None
    category_ids: Optional[List[int]] = None


class PostOut(BaseModel):
    id: int
    title: str
    description: str
    content_blocks: List[ContentBlock]
    categories: List[CategoryOut]
    image_path: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
