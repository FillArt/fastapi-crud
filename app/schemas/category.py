from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    category_id: int
    name: str

class CategoryWithCount(CategoryBase):
    post_count: int

class CategoryUpdate(BaseModel):
    name: Optional[str]

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    pk_id: int

    model_config = ConfigDict(from_attributes=True)

