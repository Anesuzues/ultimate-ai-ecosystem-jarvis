@echo off
echo 🚀 Starting Supabase for Ultimate Superagent
echo ==========================================

echo Checking Supabase CLI...
supabase --version
if %errorlevel% neq 0 (
    echo ❌ Supabase CLI not found
    echo Install with: npm install -g supabase
    pause
    exit /b 1
)

echo Starting Supabase services...
supabase start

if %errorlevel% eq 0 (
    echo.
    echo ✅ Supabase started successfully!
    echo.
    echo 📊 Dashboard: http://localhost:54323
    echo 🔌 API: http://localhost:54321
    echo 📡 Real-time: ws://localhost:54321/realtime/v1/websocket
    echo.
    echo Press any key to view status...
    pause >nul
    supabase status
) else (
    echo ❌ Failed to start Supabase
    echo Check the error messages above
)

echo.
echo Press any key to exit...
pause >nul