from typing import Optional, List, Union
from pydantic import BaseModel, ConfigDict
from app.models.content import ContentType


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


class PostContentUpdate(BaseModel):
    type: Optional[ContentType] = None
    value: Optional[ValueType] = None
    order: Optional[int] = None


class PostContentCreate(BaseModel):
    type: ContentType
    value: ValueType
    order: int

class PostContentOut(PostContentBase):
    pk_id: int

    model_config = ConfigDict(from_attributes=True)