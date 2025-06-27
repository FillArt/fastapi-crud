from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class ContactCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    institution: Optional[str]
    about: Optional[str]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Имя",
                "age": 20,
                "email": "artiom.filipopovschii@gmail.com",
                "institution": "Lorem",
                "about": "Lorem ipsum dolor sit amet",
            }
        }
    )

class ContactRead(ContactCreate):
    id: int
    file_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ContactUpload(BaseModel):
    file_path: str