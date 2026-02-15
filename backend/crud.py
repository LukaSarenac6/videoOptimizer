from sqlmodel import Session, select
from models import *
from schemas import *
from fastapi import UploadFile
from storage import *
from sqlalchemy.orm import selectinload
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def create_video(session: Session, id_sub_category: int, file: UploadFile) -> Video:
    db_video = Video (
        title=file.filename.split('.')[0],
        id_subcategory=id_sub_category,
        file_name=file.filename,
        file_ext="mp4"
    )
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    save_video(file, db_video.subcategory.name, db_video.subcategory.category.name)
    return db_video

def create_sub_category(session: Session, sub_category: SubCategoryCreate):
    db_sub_category = SubCategory(
        name=sub_category.name,
        id_category=sub_category.id_category
    )
    session.add(db_sub_category)
    session.commit()
    session.refresh(db_sub_category)
    return db_sub_category

def create_category(session: Session, category: CategoryCreate):
    db_category = Category(
        name = category.name
    )
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

def get_videos(session: Session):
    statement = select(Video)
    return session.exec(statement).all()

def get_sub_categories(session: Session):
    statement = select(SubCategory)
    return session.exec(statement).all()

def get_categories(session: Session):
    statement = select(Category).options(selectinload(Category.sub_categories))
    return session.exec(statement).all()

def create_user(session: Session, user: UserCreate) -> User:
    db_user = User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        hashed_password=password_hash.hash(user.password),
        is_admin=False,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not password_hash.verify(password, user.hashed_password):
        return None
    return user