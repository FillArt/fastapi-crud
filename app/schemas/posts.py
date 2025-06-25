from typing import List, Optional, Union, Literal
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.models.posts import ContentType


class PostBase(BaseModel):
    title: str
    description: str
    categories: Optional[List[int]] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[List[int]] = None
    image_path: Optional[str] = None

class PostOut(PostBase):
    pk_id: int
    image_path: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

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

class ListValue(BaseModel):
    list: List[str]

ValueType = Union[TextValue, TitleValue, QuoteValue, ImageValue, ListValue]

class MessageResponse(BaseModel):
    detail: str

class PostContentBase(BaseModel):
    type: ContentType
    value: ValueType
    order: int

class PostContentCreate(PostContentBase):
    pass

class PostContentOut(PostContentBase):
    pk_id: int

    model_config = ConfigDict(from_attributes=True)