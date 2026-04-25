@echo off
echo 🚀 Starting Ultimate Superagent with Supabase
echo =============================================

echo Step 1: Starting Supabase...
call start-supabase.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to start Supabase
    pause
    exit /b 1
)

echo.
echo Step 2: Testing Supabase connection...
python test-supabase-connection.py
if %errorlevel% neq 0 (
    echo ❌ Supabase connection test failed
    echo Please check your configuration
    pause
    exit /b 1
)

echo.
echo Step 3: Starting Bot-ANX Backend...
cd bot-anx\backend
start "Bot-ANX Backend" cmd /k "uvicorn server:app --port 8001 --reload --env-file .env.supabase"
cd ..\..

echo.
echo Step 4: Starting Superagent Coordinator...
timeout /t 3 >nul
start "Superagent Coordinator" cmd /k "cargo run --bin superagent-coordinator -- start --config superagent-config-supabase.json"

echo.
echo ✅ Ultimate Superagent started successfully!
echo.
echo 🌐 Services:
echo   📊 Supabase Dashboard: http://localhost:54323
echo   🔌 Supabase API: http://localhost:54321
echo   🤖 Bot-ANX Backend: http://localhost:8001
echo   ⚡ Coordinator: http://localhost:8002
echo.
echo 📱 Real-time monitoring:
echo   - Watch live updates in Supabase Dashboard
echo   - Monitor API calls and performance
echo   - Track workflow progress in real-time
echo.
echo Press any key to open dashboard...
pause >nul
start http://localhost:54323

echo.
echo 🎉 Your Ultimate Superagent is now running at full capacity!
echo Press any key to exit (services will continue running)...
pause >nul