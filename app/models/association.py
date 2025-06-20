from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.database import Base

post_category = Table(
    "post_category",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.category_id"), primary_key=True)
)
