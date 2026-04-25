@echo off
REM ============================================================
REM  JARVIS — local launcher for Windows
REM  Opens MongoDB, FastAPI backend, and React frontend in 3 windows
REM ============================================================
setlocal
set ROOT=%~dp0..
set BACKEND=%ROOT%\backend
set FRONTEND=%ROOT%\frontend
set MONGO_DATA=C:\data\db

if not exist "%MONGO_DATA%" mkdir "%MONGO_DATA%"

echo Starting MongoDB...
start "JARVIS-MongoDB" cmd /k "mongod --dbpath %MONGO_DATA% --bind_ip_all"
timeout /t 3 /nobreak > nul

echo Starting backend...
start "JARVIS-Backend" cmd /k "cd /d %BACKEND% && .venv\Scripts\activate && uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
timeout /t 4 /nobreak > nul

echo Starting frontend...
start "JARVIS-Frontend" cmd /k "cd /d %FRONTEND% && yarn start"

echo.
echo All three components launched.
echo Wait until you see "Compiled successfully" in the JARVIS-Frontend window.
echo Then open http://localhost:3000 (or this PC's LAN IP from your phone).
echo.
endlocal
