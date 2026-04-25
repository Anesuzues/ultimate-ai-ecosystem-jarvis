@echo off
echo Starting ANX + Superagent Hybrid System
echo =======================================

echo Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama is running
) else (
    echo ⚠️ Start Ollama with: ollama serve
)

echo.
echo Starting Superagent backend...
start "Superagent API" cmd /k "cd bot-anx\backend && python -m uvicorn server:app --port 8001 --reload --env-file .env.supabase"

echo.
echo ✅ Hybrid system ready!
echo 🏠 Use ANX in your terminal for local AI
echo ☁️ Use API at http://localhost:8001 for cloud features
echo 📊 Monitor at https://supabase.com/dashboard/project/heeshlozzipoullvnbja
pause
