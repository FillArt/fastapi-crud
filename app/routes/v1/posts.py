from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.params import File, Path, Body
from sqlalchemy.orm import Session
from typing import List

from app.models.posts import PostContent
from app.schemas.posts import PostOut, PostUpdate, PostContentOut, PostContentCreate, MessageResponse, PostContentUpdate
from app.services.posts import get_posts, create_post, get_post, delete_post, update_post, picture_upload, \
    create_content, get_content, delete_content, delete_all_post_content, get_content_one, update_content
from app.schemas import PostCreate
from app.db.database import get_db

router = APIRouter()

@router.get("/", response_model=List[PostOut], tags=["Posts"], summary="Get all posts")
def read_posts(db: Session = Depends(get_db)):
    return get_posts(db)

@router.post("/", response_model=PostOut, tags=["Posts"], summary="Create a new post")
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)

@router.get("/{pk_id}", response_model=PostOut, tags=["Posts"], summary="Get post by ID")
def read_post(pk_id: int, db: Session = Depends(get_db)):
    post = get_post(db, pk_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/{pk_id}/upload", response_model=PostOut, tags=["Posts"], summary="Upload picture for post by ID")
async def upload_picture_by_id(pk_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await picture_upload(db, pk_id, file)

@router.delete("/{pk_id}", tags=["Posts"], summary="Delete a post by ID")
def delete_post_by_id(pk_id: int, db: Session = Depends(get_db)):
    post = delete_post(db, pk_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.patch("/{pk_id}", response_model=PostOut, tags=["Posts"], summary="Update a post by ID")
def update_post_by_id(pk_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    updated_post = update_post(db, pk_id, post)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post

@router.post("/{post_id}/content/", response_model=PostContentOut, tags=["Posts"], summary="Create a new content for post")
def create_content_for_post(
    post_id: int = Path(..., description="ID поста"),
    content: PostContentCreate = Body(...),
    db: Session = Depends(get_db)
):
    new_content = create_content(db, post_id, content)
    if new_content is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return new_content

@router.get("/{post_id}/content/", response_model=List[PostContentOut], tags=["Posts"], summary="Get all content by ID post")
def get_content_for_post(post_id: int, db: Session = Depends(get_db)):
    post_content = get_content(db, post_id)
    if not post_content:
        return []
    return post_content

@router.get("/{post_id}/{content_id}/content", response_model=PostContentOut, tags=["Posts"], summary="Get content by ID")
def get_content_by_content_id(post_id: int, content_id: int, db: Session = Depends(get_db)):
    post_content = get_content_one(db, content_id)
    if not post_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return post_content

@router.delete("/{post_id}/{content_id}/content/", response_model=PostContentOut, tags=["Posts"], summary="Delete a content by ID content")
def delete_content_for_post( content_id: int, post_id: int, db: Session = Depends(get_db)):
    content = delete_content(db, content_id)
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.delete('/{post_id}/content/', response_model=MessageResponse, tags=["Posts"],
               summary="Delete a content by ID")
def delete_all_content_for_post(post_id: int, db: Session = Depends(get_db)):
    count = delete_all_post_content(db, post_id)
    if count is None:
        raise HTTPException(status_code=404, detail="No content found for this post")
    return count


@router.patch("/{post_id}/{content_id}/content/", response_model=PostContentOut, tags=["Posts"], summary="Delete a content by ID content")
def update_content_for_post( content_id: int, data: PostContentUpdate, post_id: int, db: Session = Depends(get_db)):
    content = update_content(db, content_id, data)
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content