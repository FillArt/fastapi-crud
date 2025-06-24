from typing import List, Optional, Union, Literal
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.schemas.category import CategoryOut


class ListValue(BaseModel):
    list: List[str]


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


ValueType = Union[TextValue, TitleValue, QuoteValue, ImageValue, ListValue]

class ContentBlock(BaseModel):
    id: int
    type: Literal["text", "title", "quote", "image", "list"]
    value: ValueType
    order: int


class PostBase(BaseModel):
    title: str
    description: str
    categories: List[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    categories: List[str] = None
    image_path: Optional[str] = None


class PostOut(BaseModel):
    pk_id: int
    title: str
    description: str
    categories: List[int] = None
    image_path: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
