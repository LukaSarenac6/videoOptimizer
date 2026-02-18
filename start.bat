@echo off
echo Starting Human Performance Lab...
echo.

start "Backend - FastAPI" cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --reload --port 8000"
start "Frontend - Vite" cmd /k "cd /d %~dp0frontend\my-app && npm run dev"

echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Both servers started in separate windows.
