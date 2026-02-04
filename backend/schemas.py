from sqlmodel import SQLModel
from typing import Optional
from models import *

class VideoCreate(SQLModel):
    title: str
    id_sub_category: int

class VideoRead(SQLModel):
    id: int
    title: str
    file_name: str
    file_ext: str
    subcategory: Optional[SubCategory]

class CategoryCreate(SQLModel):
    name: str

class CategoryRead(SQLModel):
    name: str
    id: int
    sub_categories: list[SubCategory] = []

class SubCategoryCreate(SQLModel):
    name: str
    id_category: int

class SubCategoryRead(SQLModel):
    name: str
    id: int
    id_category: int
    category: Category