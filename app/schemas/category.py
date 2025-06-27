from typing import Optional
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str

class CategoryWithCount(CategoryBase):
    post_count: int

class CategoryUpdate(BaseModel):
    name: Optional[str]
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Тестовая категория",
            }
        }
    )

class CategoryCreate(CategoryBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Тестовая категория",
            }
        }
    )

class CategoryOut(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

