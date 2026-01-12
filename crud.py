from sqlmodel import Session, select
from models import Video
from schemas import VideoCreate

def create_video(session: Session, video: VideoCreate) -> Video:
    db_video = Video.model_validate(video)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

def get_videos(session: Session):
    statement = select(Video)
    return session.exec(statement).all()