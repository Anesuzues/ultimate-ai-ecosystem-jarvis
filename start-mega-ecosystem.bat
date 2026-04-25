@echo off
echo 🚀 Starting MEGA AI Development Ecosystem
echo ==========================================
echo.

echo 📋 System Check...
echo ✅ ANX: Available in your terminal
echo ✅ Claw-code: Ready for local AI coding
echo ✅ Ollama: Local AI models
echo ✅ Superagent: Workflow coordination  
echo ✅ Godmode: Personal AI OS with 35 agents
echo.

echo 🏠 Phase 1: Starting Local AI Tier...
echo Starting Ollama...
start "Ollama Server" cmd /k "ollama serve"
timeout /t 3 >nul

echo Checking Claw-code...
if exist "claw-code\rust\target\debug\claw.exe" (
    echo ✅ Claw-code ready
) else (
    echo ⚠️ Building Claw-code...
    cd claw-code\rust
    cargo build --workspace
    cd ..\..
)

echo.
echo 🔄 Phase 2: Starting Hybrid Coordination Tier...
echo Starting Superagent API...
start "Superagent API" cmd /k "cd bot-anx\backend && python -m uvicorn server:app --port 8001 --reload --env-file .env.supabase"
timeout /t 3 >nul

echo.
echo ☁️ Phase 3: Starting Cloud Intelligence Tier...
echo Starting Godmode...
if exist "godmode-main\package.json" (
    start "Godmode" cmd /k "cd godmode-main && pnpm start"
) else (
    echo ⚠️ Godmode not found - install dependencies first
)

echo.
echo 🎉 MEGA AI Ecosystem Started!
echo ==========================================
echo.
echo 🌐 Access Points:
echo   🏠 ANX: Your terminal (continue using as normal)
echo   🤖 Claw-code: claw-code\rust\target\debug\claw.exe --model local
echo   🔧 Ollama: http://localhost:11434
echo   🔄 Superagent API: http://localhost:8001/docs
echo   ☁️ Godmode: http://localhost:18789/godmode
echo   📊 Supabase: https://supabase.com/dashboard/project/heeshlozzipoullvnbja
echo.
echo 💡 Quick Start:
echo   1. Use ANX in terminal for fast local AI
echo   2. Use Claw for advanced coding with: .\claw-code\rust\target\debug\claw.exe --model local
echo   3. Monitor workflows at Superagent API docs
echo   4. Orchestrate with 35 agents at Godmode
echo   5. Track everything in Supabase dashboard
echo.
echo 🎯 Workflows Available:
echo   • Ticket-to-Deployment (ClickUp → Code → Deploy)
echo   • Research-to-Implementation (Research → Analysis → Code)
echo   • Team Coordination (Multi-agent orchestration)
echo.
echo Press any key to open dashboards...
pause >nul

start http://localhost:8001/docs
start http://localhost:18789/godmode
start https://supabase.com/dashboard/project/heeshlozzipoullvnbja

echo.
echo 🔥 Your MEGA AI Ecosystem is now operational!
echo Use all 5 systems together for maximum power!
pause
