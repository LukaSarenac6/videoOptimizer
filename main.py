from fastapi import FastAPI, Depends
from sqlmodel import Session

from database import engine, create_db_and_tables
from schemas import *
from crud import *

app = FastAPI()
create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/videos", response_model=VideoRead)
def add_video(
    video: VideoCreate,
    session: Session = Depends(get_session)
):
    return create_video(session, video)

@app.get("/videos", response_model=list[VideoRead])
def read_videos(
    session: Session = Depends(get_session)
):
    return get_videos(session)

@app.post("/sub_category", response_model=SubCategoryRead)
def add_sub_category(
    sub_category: SubCategoryCreate,
    session: Session = Depends(get_session)
):
    return create_sub_category(session, sub_category)

@app.get("/sub_categories", response_model=list[SubCategory])
def read_sub_categories(
    session: Session = Depends(get_session)
):
    return get_sub_categories(session)
