from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    last_name: str
    middle_name: Optional[str]
    profession: Optional[str]

class AuthorCreate(AuthorBase):
    pass

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Имя",
                "last_name": "Фамилия",
                "middle_name": "Отчество",
                "profession": "Профессия",
            }
        }
    )

class AuthorUpdate(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    profession: Optional[str]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Имя",
                "last_name": "Фамилия",
                "middle_name": "Отчество",
                "profession": "Профессия",
            }
        }
    )

class AuthorOut(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
