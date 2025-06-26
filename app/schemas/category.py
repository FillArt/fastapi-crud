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
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "category_id": 888,
                "description": "Тестовая категория",
            }
        }
    )

class CategoryOut(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

