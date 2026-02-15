from fastapi import FastAPI, Depends, UploadFile, Form, HTTPException
from sqlmodel import Session
from typing import Annotated
from database import engine, create_db_and_tables
from schemas import *
from crud import *
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

create_db_and_tables()

# --- Dependencies ---

def get_session():
    with Session(engine) as session:
        yield session

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # TODO: replace with real JWT decoding
    pass

# --- Auth ---

@app.post("/register", response_model=UserRead)
def register(
    user: UserCreate,
    session: Session = Depends(get_session),
):
    existing = get_user_by_email(session, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(session, user)

# --- Categories ---

@app.post("/category", response_model=CategoryRead)
def add_category(
    category: CategoryCreate,
    session: Session = Depends(get_session),
):
    return create_category(session, category)

@app.get("/categories", response_model=list[CategoryRead])
def read_categories(
    session: Session = Depends(get_session),
):
    return get_categories(session)

# --- Sub Categories ---

@app.post("/sub_category", response_model=SubCategoryRead)
def add_sub_category(
    sub_category: SubCategoryCreate,
    session: Session = Depends(get_session),
):
    return create_sub_category(session, sub_category)

@app.get("/sub_categories", response_model=list[SubCategory])
def read_sub_categories(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    return get_sub_categories(session)

# --- Videos ---

@app.post("/video", response_model=VideoRead)
def add_video(
    id_sub_category: Annotated[int, Form()],
    file: UploadFile,
    session: Session = Depends(get_session),
):
    return create_video(session, id_sub_category, file)

@app.post("/videos", response_model=list[VideoRead])
def add_videos(
    # TODO: Swagger stores list[int] as "1,1,1" causing 422. Using str workaround.
    id_sub_category_str: Annotated[str, Form()],
    files: list[UploadFile],
    session: Session = Depends(get_session),
):
    id_sub_category = [int(x) for x in id_sub_category_str.split(',')]
    if len(id_sub_category) != len(files):
        raise HTTPException(
            status_code=400,
            detail="Each file must have a corresponding sub-category",
        )
    videos = []
    try:
        for sub_id, file in zip(id_sub_category, files):
            video = create_video(session, sub_id, file)
            videos.append(video)
        return videos
    except Exception:
        session.rollback()
        raise

@app.get("/videos", response_model=list[VideoRead])
def read_videos(
    session: Session = Depends(get_session),
):
    return get_videos(session)
