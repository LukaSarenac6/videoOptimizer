from sqlmodel import Session, select
from models import *
from schemas import *

def create_video(session: Session, video: VideoCreate) -> Video:
    db_video = Video (
        title=video.title,
        id_subcategory=video.id_sub_category,
        file_name=f"{video.title}.mp4",
        file_ext="mp4"
    )
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

def create_category(session: Session, category: CategoryCreate):
    db_category = Category(
        name=category.name
    )
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

def create_sub_category(session: Session, sub_category: SubCategoryCreate):
    db_sub_category = SubCategory(
        name=sub_category.name,
        id_category=sub_category.id_category
    )
    session.add(db_sub_category)
    session.commit()
    session.refresh(db_sub_category)
    return db_sub_category

def get_videos(session: Session):
    statement = select(Video)
    return session.exec(statement).all()