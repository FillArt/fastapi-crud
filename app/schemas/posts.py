from pydantic import BaseModel

class PostSchema(BaseModel):
    title: str
    description: str
    content: str

class PostResponseSchema(PostSchema):
    id: int

    class Config:
        orm_mode = True