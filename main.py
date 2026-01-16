from fastapi import FastAPI, Depends
from sqlmodel import Session

from database import engine, create_db_and_tables
from schemas import *
from crud import create_video, get_videos

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
