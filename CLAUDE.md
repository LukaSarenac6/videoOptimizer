# Human Performance Lab - Project Instructions

## Project Stack
- **Backend**: FastAPI + SQLModel + SQLite (Python)
- **Frontend**: Vite + React + TypeScript
- **Auth**: JWT (PyJWT), password hashing (pwdlib)

## Rules

### Dependencies
- When installing any new library, ALWAYS update:
  - `README.md` dependencies table (with install command)
  - `backend/requirements.txt` (Python) or `frontend/my-app/package.json` (JS)

### Plans
- Store implementation plans in `plans/` folder
- Format: `plans/YYYY-MM-DD-short-description.md`

### Shell Commands (Windows)
- NEVER redirect to NUL or /dev/null
- Always quote paths with double quotes

## Key Files
- `backend/main.py` - API endpoints
- `backend/auth.py` - JWT auth, get_current_user, get_admin_user
- `backend/crud.py` - DB operations
- `backend/models.py` - User, Athlete, Category, SubCategory, Video
- `backend/schemas.py` - Pydantic schemas
- `backend/create_admin.py` - Seed script for first admin
- `frontend/my-app/src/context/AuthContext.tsx` - Auth state management
- `frontend/my-app/src/api/` - API layer (client, auth, athletes)

## Auth Flow
- `POST /token` (public) - login, returns JWT
- `GET /me` (protected) - validate token, return user info
- `POST /register` (admin only) - create new coach accounts
- All other endpoints require `get_current_user`
- First admin created via `python create_admin.py`
