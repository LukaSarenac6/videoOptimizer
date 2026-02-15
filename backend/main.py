from fastapi import FastAPI, Depends, UploadFile, Form, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from database import engine, create_db_and_tables
from schemas import *
from crud import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import *
from datetime import datetime, timedelta, timezone
import jwt

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

create_db_and_tables()

# --- Dependencies ---

def get_session():
    with Session(engine) as session:
        yield session

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user_by_email(session, email)
    if user is None:
        raise credentials_exception
    return user

# --- Auth (public) ---

# Register a new coach account
@app.post("/register", response_model=UserRead)
def register(
    user: UserCreate,
    session: Session = Depends(get_session),
):
    existing = get_user_by_email(session, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(session, user)

# Login with email and password, returns JWT access token
@app.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# --- Categories (protected) ---

# Create a new category
@app.post("/category", response_model=CategoryRead)
def add_category(
    category: CategoryCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    return create_category(session, category)

# Get all categories with their sub-categories
@app.get("/categories", response_model=list[CategoryRead])
def read_categories(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    return get_categories(session)

# --- Sub Categories (protected) ---

# Create a new sub-category under a category
@app.post("/sub_category", response_model=SubCategoryRead)
def add_sub_category(
    sub_category: SubCategoryCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    return create_sub_category(session, sub_category)

# Get all sub-categories
@app.get("/sub_categories", response_model=list[SubCategory])
def read_sub_categories(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    return get_sub_categories(session)

# --- Videos (protected) ---

# Upload a single video to a sub-category
@app.post("/video", response_model=VideoRead)
def add_video(
    id_sub_category: Annotated[int, Form()],
    file: UploadFile,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    return create_video(session, id_sub_category, file)

# Upload multiple videos with corresponding sub-category IDs
@app.post("/videos", response_model=list[VideoRead])
def add_videos(
    # TODO: Swagger stores list[int] as "1,1,1" causing 422. Using str workaround.
    id_sub_category_str: Annotated[str, Form()],
    files: list[UploadFile],
    current_user: Annotated[User, Depends(get_current_user)],
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

# Get all videos
@app.get("/videos", response_model=list[VideoRead])
def read_videos(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    return get_videos(session)

# --- Athletes (protected) ---

# Add a new athlete
@app.post("/athlete", response_model=AthleteRead)
def add_athlete(
    athlete: AthleteCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    return create_athlete(session, athlete)

# Get all athletes
@app.get("/athletes", response_model=list[AthleteRead])
def read_athletes(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    return get_athletes(session)
