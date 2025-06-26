from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Path, Body
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.content import PostContentOut, PostContentCreate, MessageResponse, PostContentUpdate
from app.services.content import create_content, get_content, get_content_one, delete_content, delete_all_post_content, \
    update_content

router = APIRouter()


@router.post("/{post_id}/content/", response_model=PostContentOut, tags=["Content"], openapi_extra={
    "requestBody": {
        "content": {
            "application/json": {
                "examples": {
                    "TitleExample": {
                        "summary": "Заголовок",
                        "value": {
                            "type": "title",
                            "value": {
                                "title": "Привет, мир!"
                            },
                            "order": 1
                        }
                    },
                    "TextExample": {
                        "summary": "Текст",
                        "value": {
                            "type": "text",
                            "value": {
                                "content": "Привет, мир!"
                            },
                            "order": 2
                        }
                    },
                    "ImageExample": {
                        "summary": "Картинка",
                        "value": {
                            "type": "image",
                            "value": {
                                "url": "https://example.com/image.jpg",
                                "title": "Здесь будет какой нибудь заголовок",
                                "text": "Какой-то текст...",
                                "alt": "Пример картинки"
                            },
                            "order": 3
                        }
                    },
                    "QuoteExample": {
                        "summary": "Цитата",
                        "value": {
                            "type": "quote",
                            "value": {
                                "content": "Крутая цитата",
                                "author": "Не менее крутой автор"
                            },
                            "order": 4
                        }
                    },
                    "ListExample": {
                        "summary": "Список",
                        "value": {
                            "type": "list",
                            "value": {
                                "list": [
                                    'Первый пункт',
                                    'Второй пункт',
                                    'Третий пункт'
                                ]
                            },
                            "order": 5
                        }
                    },
                }
            }
        }
    }
}, summary="Create a new content for post")
def create_content_for_post(
        post_id: int = Path(..., description="ID поста"),
        content: PostContentCreate = Body(...),
        db: Session = Depends(get_db)
):
    new_content = create_content(db, post_id, content)
    if new_content is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return new_content


@router.get("/{post_id}/content/", response_model=List[PostContentOut], tags=["Content"],
            summary="Get all content by ID post")
def get_content_for_post(post_id: int, db: Session = Depends(get_db)):
    post_content = get_content(db, post_id)
    if not post_content:
        return []
    return post_content


@router.get("/{post_id}/{content_id}/content", response_model=PostContentOut, tags=["Content"],
            summary="Get content by ID")
def get_content_by_content_id(post_id: int, content_id: int, db: Session = Depends(get_db)):
    post_content = get_content_one(db, content_id)
    if not post_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return post_content


@router.delete("/{post_id}/{content_id}/content/", response_model=PostContentOut, tags=["Content"],
               summary="Delete a content by ID content")
def delete_content_for_post(content_id: int, post_id: int, db: Session = Depends(get_db)):
    content = delete_content(db, content_id)
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.delete('/{post_id}/content/', response_model=MessageResponse, tags=["Content"],
               summary="Delete a content by ID")
def delete_all_content_for_post(post_id: int, db: Session = Depends(get_db)):
    count = delete_all_post_content(db, post_id)
    if count is None:
        raise HTTPException(status_code=404, detail="No content found for this post")
    return count


@router.patch("/{post_id}/{content_id}/content/", response_model=PostContentOut, tags=["Content"],
              summary="Update a content by ID content")
def update_content_for_post(content_id: int, data: PostContentUpdate, post_id: int, db: Session = Depends(get_db)):
    content = update_content(db, content_id, data)
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content
