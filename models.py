from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# To handle MongoDB's ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class BlogPostBase(BaseModel):
    title: str
    content: str
    author: str
    tags: Optional[list[str]] = []

    class Config:
        arbitrary_types_allowed = True

class BlogPostDB(BlogPostBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
