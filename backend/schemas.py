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

class UserCreate(SQLModel):
    name: str
    surname: str
    email: str
    password: str

class UserRead(SQLModel):
    id: int
    name: str
    surname: str
    email: str
    is_admin: bool

class AthleteCreate(SQLModel):
    name: str
    surname: str
    email: str

class AthleteRead(SQLModel):
    id: int
    name: str
    surname: str
    email: str

class Token(SQLModel):
    access_token: str
    token_type: str