from sqlmodel import SQLModel, Field, Relationship

class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    sub_categories: list["SubCategory"] = Relationship(back_populates="category")

class SubCategory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    id_category: int | None = Field(default=None, foreign_key="category.id")
    category: Category | None = Relationship(back_populates="sub_categories")

    videos: list["Video"] = Relationship(back_populates="subcategory")

class Video(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    file_name: str
    file_ext: str

    id_subcategory: int | None = Field(default=None, foreign_key="subcategory.id")
    subcategory: SubCategory = Relationship(back_populates="videos")

class Athlete(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    surname: str
    email: str
    phone_number: str

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    surname: str
    hashed_password: str
    is_admin: bool

    email: str