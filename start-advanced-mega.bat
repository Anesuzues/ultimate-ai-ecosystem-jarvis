@echo off
echo Advanced MEGA AI Ecosystem Startup
echo ==================================
echo.

echo Phase 1: Local AI Tier (Advanced)
echo Starting Ollama with advanced features...
start "Ollama Advanced" cmd /k "ollama serve"
timeout /t 3 >nul

echo Building Claw-code with advanced features...
if not exist "claw-code\rust\target\debug\claw.exe" (
    echo Building Claw-code...
    cd claw-code\rust
    cargo build --workspace --release
    cd ..\..
)

echo Phase 2: Hybrid Coordination (Advanced)
echo Starting Superagent with advanced workflows...
start "Superagent Advanced" cmd /k "cd bot-anx\backend && python -m uvicorn server:app --port 8001 --reload --env-file .env.supabase"

echo Phase 3: Personal AI OS (Advanced)
echo Starting Godmode with 35 specialist agents...
if exist "godmode-main\package.json" (
    cd godmode-main
    if not exist "node_modules" (
        echo Installing Godmode dependencies...
        pnpm install
    )
    start "Godmode AI OS" cmd /k "pnpm start"
    cd ..
)

echo.
echo Advanced MEGA AI Ecosystem Online!
echo =================================
echo.
echo Local AI Tier:
echo   ANX: Terminal AI assistant
echo   Claw-code: Advanced AI development environment
echo   Ollama: Local AI models with optimization
echo.
echo Hybrid Coordination:
echo   Superagent: Workflow orchestration + Supabase
echo   Real-time: Live progress tracking
echo.
echo Personal AI OS:
echo   Godmode: 35 specialist agents
echo   Project orchestration and delegation
echo   Overnight optimization system
echo   Memory systems and skill cards
echo.
echo Advanced Features Enabled:
echo   Session persistence and management
echo   Intelligent task routing
echo   Quality gates and TDD enforcement
echo   Agent delegation system
echo   Overnight optimization
echo   Trust tracking system
echo   Real-time collaboration
echo.
echo Access Points:
echo   ANX: Your terminal
echo   Claw: .\claw-code\rust\target\debug\claw.exe --model local
echo   Ollama: http://localhost:11434
echo   Superagent: http://localhost:8001/docs
echo   Godmode: http://localhost:18789/godmode
echo   Supabase: https://supabase.com/dashboard/project/heeshlozzipoullvnbja
echo.
echo Press any key to open all dashboards...
pause >nul

start http://localhost:8001/docs
start http://localhost:18789/godmode
start https://supabase.com/dashboard/project/heeshlozzipoullvnbja

echo.
echo Your Advanced MEGA AI Ecosystem is operational!
pause
