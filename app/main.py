from fastapi import FastAPI
from app.api.v1 import posts, contact
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine

import uvicorn
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:4321",
    "http://127.0.0.1:4321",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact.router, prefix="/api/v1/contact", tags=["Contact"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["Posts"])

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
