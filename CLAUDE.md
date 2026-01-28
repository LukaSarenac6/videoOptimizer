# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Video Optimizer API - A FastAPI backend for managing videos organized by categories and subcategories.

## Tech Stack

- **Python 3.13.5** with **FastAPI 0.128.0**
- **SQLModel 0.0.31** (combines SQLAlchemy ORM + Pydantic validation)
- **SQLite** database (database.db)
- **Uvicorn** ASGI server

## Common Commands

```bash
# Run development server with hot reload
uvicorn main:app --reload

# Alternative: run with FastAPI CLI
fastapi run main.py
```

The API serves interactive docs at `/docs` (Swagger) and `/redoc`.

## Architecture

Layered architecture with clear separation of concerns:

```
main.py      → HTTP route handlers, dependency injection
crud.py      → Database operations (create/read functions)
models.py    → SQLModel ORM entities with relationships
schemas.py   → Pydantic request/response validation schemas
database.py  → SQLite engine configuration
```

## Data Model

Three-tier hierarchy with foreign key relationships:

```
Category (1) → (N) SubCategory (1) → (N) Video
```

- **Category**: id, name
- **SubCategory**: id, name, id_category (FK)
- **Video**: id, title, file_name, file_ext, id_subcategory (FK)

## Current API Endpoints

- `POST /videos` - Create video
- `GET /videos` - List all videos
- `POST /sub_category` - Create subcategory
- `GET /sub_categories` - List all subcategories

Note: Category endpoints not yet implemented.

## Dependencies

Not tracked in repo (no requirements.txt/pyproject.toml). Install manually:
```bash
pip install fastapi sqlmodel uvicorn
```
