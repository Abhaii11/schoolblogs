from fastapi import FastAPI, HTTPException, Depends
from typing import List
from bson import ObjectId
from models import BlogPostBase, BlogPostDB
from database import db

app = FastAPI()

# Helper to transform MongoDB ObjectId into JSON-friendly format
def blogpost_entity(blogpost) -> dict:
    return {**blogpost, "id": str(blogpost["_id"])}

@app.post("/blogs/", response_model=BlogPostDB)
async def create_blog(blog: BlogPostBase):
    blog = blog.dict()
    result = await db.blogs.insert_one(blog)
    created_blog = await db.blogs.find_one({"_id": result.inserted_id})
    return blogpost_entity(created_blog)

@app.get("/blogs/{id}", response_model=BlogPostDB)
async def get_blog(id: str):
    blog = await db.blogs.find_one({"_id": ObjectId(id)})
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blogpost_entity(blog)

@app.get("/blogs/", response_model=List[BlogPostDB])
async def list_blogs():
    blogs = await db.blogs.find().to_list(100)
    return [blogpost_entity(blog) for blog in blogs]

@app.put("/blogs/{id}", response_model=BlogPostDB)
async def update_blog(id: str, blog: BlogPostBase):
    result = await db.blogs.update_one({"_id": ObjectId(id)}, {"$set": blog.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    updated_blog = await db.blogs.find_one({"_id": ObjectId(id)})
    return blogpost_entity(updated_blog)

@app.delete("/blogs/{id}", status_code=204)
async def delete_blog(id: str):
    result = await db.blogs.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
