@echo off
echo 🌐 Starting Ultimate Superagent with Cloud Supabase
echo ================================================

echo Step 1: Testing Supabase connection...
python test-supabase-connection.py
if %errorlevel% neq 0 (
    echo.
    echo ⚠️ Supabase connection failed. Please:
    echo 1. Create Supabase project at https://supabase.com/dashboard
    echo 2. Update bot-anx/backend/.env.supabase with your project details
    echo 3. Apply schema from supabase-schema.sql in SQL Editor
    echo.
    echo See SETUP_CLOUD_SUPABASE.md for detailed instructions
    pause
    exit /b 1
)

echo.
echo Step 2: Starting Bot-ANX Backend...
cd bot-anx\backend
start "Bot-ANX Backend" cmd /k "python -m uvicorn server:app --port 8001 --reload --env-file .env.supabase"
cd ..\..

echo.
echo ✅ Ultimate Superagent started with Cloud Supabase!
echo.
echo 🌐 Services:
echo   📊 Supabase Dashboard: Check your project URL
echo   🤖 Bot-ANX API: http://localhost:8001/docs
echo.
echo 📱 Real-time monitoring:
echo   - Watch live updates in Supabase Dashboard
echo   - Monitor API calls and performance
echo   - Track workflow progress in real-time
echo.
echo 📖 Setup Guide: SETUP_CLOUD_SUPABASE.md
echo.
echo Press any key to open API docs...
pause >nul
start http://localhost:8001/docs

echo.
echo 🎉 Your Ultimate Superagent is running at full capacity!
echo Press any key to exit (services will continue running)...
pause >nul