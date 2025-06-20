from pydantic import BaseModel

class CategoryBase(BaseModel):
    category_id: int
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    class Config:
        orm_mode = True
