from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

class PostSchema(BaseModel):
    title: str
    description: str
    content: str

posts = [
    {
        "id": 1,
        "title": "First post title",
        "description": "First post description",
        "content": "First post content",
    },
    {
        "id": 2,
        "title": "Second post title",
        "description": "Second post description",
        "content": "Second post content",
    },
    {
        "id": 3,
        "title": "Third post title",
        "description": "Third post description",
        "content": "Third post content",
    },
    {
        "id": 4,
        "title": "Fourth post title",
        "description": "Fourth post description",
        "content": "Fourth post content",
    },
]

app = FastAPI()

@app.get("/posts", tags=["Posts"], summary="Get all posts")
async def get_posts():
    if posts:
        return posts
    raise HTTPException(status_code=404, detail="No posts found")

@app.post("/posts", tags=["Posts"], summary="Post creation")
async def create_post(post: PostSchema):
    new_post = {
        "id": len(posts) + 1,
        "title": post.title,
        "description": post.description,
        "content": post.content,
    }
    posts.append(new_post)
    return {"success": True, "post": new_post}

@app.get("/posts/{id}", tags=["Posts"], summary="Getting a post by id")
async def get_post(id: int):
    for post in posts:
        if post["id"] == id:
            return post
    raise HTTPException(status_code=404, detail="No post found")

@app.delete("/posts/{id}", tags=["Posts"], summary="Delete a post by id")
async def delete_post(id: int):
    index = next((i for i, post in enumerate(posts) if post["id"] == id), None)
    if index is not None:
        deleted_post = posts.pop(index)
        return {"success": True, "deleted": deleted_post}
    raise HTTPException(status_code=404, detail="Post not found")


@app.put("/posts/{id}", tags=["Posts"], summary="Update a post")
async def update_post(id: int, data: Post):
    for post in posts:
        if post["id"] == id:
            post["title"] = data.title
            post["description"] = data.description
            post["content"] = data.content
            return {"success": True, "post": post}

    raise HTTPException(status_code=404, detail="Post not found")


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
