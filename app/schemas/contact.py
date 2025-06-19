from typing import Optional
from pydantic import BaseModel, EmailStr

class ContactCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    institution: Optional[str]
    about: Optional[str]

class ContactRead(ContactCreate):
    id: int
    file_path: Optional[str] = None

    class Config:
        orm_mode = True

class ContactUpload(BaseModel):
    file_path: str