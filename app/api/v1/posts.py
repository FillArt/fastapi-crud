from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.posts import PostOut
from app.services.posts import get_posts, create_post, get_post, delete_post, update_post
from app.schemas import PostCreate, Post
from app.db.database import get_db

router = APIRouter()

@router.get("/", response_model=List[Post], tags=["Posts"], summary="Get all posts")
def read_posts(db: Session = Depends(get_db)):
    return get_posts(db)

@router.post("/", response_model=PostOut, tags=["Posts"], summary="Create a new post")
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)

@router.get("/{id}", response_model=Post, tags=["Posts"], summary="Get post by ID")
def read_post(id: int, db: Session = Depends(get_db)):
    post = get_post(db, id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{id}", tags=["Posts"], summary="Delete a post by ID")
def delete_post_by_id(id: int, db: Session = Depends(get_db)):
    post = delete_post(db, id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{id}", response_model=Post, tags=["Posts"], summary="Update a post by ID")
def update_post_by_id(id: int, post: PostCreate, db: Session = Depends(get_db)):
    post = update_post(db, id, post)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post