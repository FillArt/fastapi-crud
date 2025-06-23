from pydantic import BaseModel

class CategoryBase(BaseModel):
    category_id: int
    name: str

class CategoryWithCount(BaseModel):
    category_id: int
    name: str
    post_count: int

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    class Config:
        orm_mode = True
