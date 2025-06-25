from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class ContactCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    institution: Optional[str]
    about: Optional[str]

class ContactRead(ContactCreate):
    id: int
    file_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ContactUpload(BaseModel):
    file_path: str