# Video Optimizer

A coaching app for managing training sessions, athletes, and exercise videos. Built with FastAPI (backend) and React + Vite (frontend).

## Project Structure

```
videoOptimizer/
├── backend/           # FastAPI REST API
│   ├── main.py        # API endpoints
│   ├── auth.py        # JWT authentication & authorization
│   ├── models.py      # Database models (User, Athlete, Category, SubCategory, Video)
│   ├── schemas.py     # Request/response schemas
│   ├── crud.py        # Database operations
│   ├── config.py      # Environment variable loading
│   ├── database.py    # SQLite engine setup
│   ├── storage.py     # Video file storage
│   └── create_admin.py # One-time script to create the first admin user
├── frontend/          # React + Vite + TypeScript (on frontend branch)
│   └── my-app/
└── plans/             # Future feature plans
```

## Backend Setup

### Prerequisites
- Python 3.11+

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the `backend/` folder:

```
SECRET_KEY=<generate with: openssl rand -hex 32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Create First Admin

Before using the app, create the first admin user:

```bash
cd backend
python create_admin.py
```

This will prompt you for name, surname, email, and password. Only admin users can register new coaches via the API.

### Run

```bash
cd backend
fastapi dev main.py
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

### API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/token` | Public | Login, returns JWT token |
| POST | `/register` | Admin | Create a new coach account |
| POST | `/category` | Coach | Create a category |
| GET | `/categories` | Coach | List all categories with sub-categories |
| POST | `/sub_category` | Coach | Create a sub-category |
| GET | `/sub_categories` | Coach | List all sub-categories |
| POST | `/video` | Coach | Upload a video |
| POST | `/videos` | Coach | Upload multiple videos |
| GET | `/videos` | Coach | List all videos |
| POST | `/athlete` | Coach | Add an athlete |
| GET | `/athletes` | Coach | List all athletes |

## Frontend Setup

> Frontend is currently on the `frontend` branch.

### Prerequisites
- Node.js 18+

### Installation

```bash
cd frontend/my-app
npm install
```

### Run

```bash
cd frontend/my-app
npm run dev
```

The app will be available at `http://localhost:5173`.

## Dependencies

### Backend (Python)
| Package | Install Command | Purpose |
|---------|----------------|---------|
| fastapi | `pip install fastapi` | Web framework |
| uvicorn | `pip install uvicorn` | ASGI server |
| sqlmodel | `pip install sqlmodel` | ORM (SQLAlchemy + Pydantic) |
| python-dotenv | `pip install python-dotenv` | Load .env variables |
| PyJWT | `pip install PyJWT` | JWT token encoding/decoding |
| pwdlib[bcrypt] | `pip install "pwdlib[bcrypt]"` | Password hashing |
| python-multipart | `pip install python-multipart` | File upload support |

Or install all at once:
```bash
pip install -r backend/requirements.txt
```

### Frontend (Node.js)
| Package | Install Command | Purpose |
|---------|----------------|---------|
| react | `npm install react` | UI library |
| react-dom | `npm install react-dom` | React DOM rendering |
| react-router-dom | `npm install react-router-dom` | Client-side routing |
| vite | `npm install vite` | Build tool & dev server |
| typescript | `npm install typescript` | Type checking |

Or install all at once:
```bash
cd frontend/my-app
npm install
```
