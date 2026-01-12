from sqlmodel import SQLModel

class VideoCreate(SQLModel):
    name: str
    category: str

class VideoRead(SQLModel):
    id: int
    name: str
    category: str