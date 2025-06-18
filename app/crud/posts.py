from fastapi import HTTPException
from app.db.fake_db import posts
from app.schemas.posts import PostSchema

def get_posts():
    if posts:
        return posts
    raise HTTPException(status_code=404, detail="No posts found")


async def create_post(post: PostSchema):
    new_post = {
        "id": len(posts) + 1,
        "title": post.title,
        "description": post.description,
        "content": post.content,
    }
    posts.append(new_post)
    return {"success": True, "post": new_post}

def get_post(id: int):
    for post in posts:
        if post["id"] == id:
            return post
    raise HTTPException(status_code=404, detail="No post found")

async def delete_post(id: int):
    index = next((i for i, post in enumerate(posts) if post["id"] == id), None)
    if index is not None:
        deleted_post = posts.pop(index)
        return {"success": True, "deleted": deleted_post}
    raise HTTPException(status_code=404, detail="Post not found")

async def update_post(id: int, data: PostSchema):
    for post in posts:
        if post["id"] == id:
            post["title"] = data.title
            post["description"] = data.description
            post["content"] = data.content
            return {"success": True, "post": post}

    raise HTTPException(status_code=404, detail="Post not found")
