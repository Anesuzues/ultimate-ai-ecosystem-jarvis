# Simple Supabase Setup for Windows
Write-Host "🚀 Setting up Supabase for Ultimate Superagent" -ForegroundColor Blue

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
if (Get-Command node -ErrorAction SilentlyContinue) {
    Write-Host "✅ Node.js found" -ForegroundColor Green
    node --version
} else {
    Write-Host "❌ Node.js not found. Please install from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Install Supabase CLI
Write-Host "Installing Supabase CLI..." -ForegroundColor Yellow
if (Get-Command supabase -ErrorAction SilentlyContinue) {
    Write-Host "✅ Supabase CLI already installed" -ForegroundColor Green
} else {
    try {
        npm install -g supabase
        Write-Host "✅ Supabase CLI installed" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ NPM global install failed, trying alternative..." -ForegroundColor Yellow
        Write-Host "Please install Supabase CLI manually:" -ForegroundColor Cyan
        Write-Host "1. Download from: https://github.com/supabase/cli/releases" -ForegroundColor Cyan
        Write-Host "2. Or use: winget install Supabase.cli" -ForegroundColor Cyan
        Write-Host "3. Or use: scoop install supabase" -ForegroundColor Cyan
        Read-Host "Press Enter after installing Supabase CLI"
    }
}

# Initialize Supabase
Write-Host "Initializing Supabase project..." -ForegroundColor Yellow
if (Test-Path "supabase/config.toml") {
    Write-Host "✅ Supabase already initialized" -ForegroundColor Green
} else {
    supabase init
    Write-Host "✅ Supabase initialized" -ForegroundColor Green
}

# Create migrations directory
if (!(Test-Path "supabase/migrations")) {
    New-Item -ItemType Directory -Path "supabase/migrations" -Force
}

# Copy schema
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
Copy-Item "supabase-schema.sql" "supabase/migrations/${timestamp}_initial_schema.sql"
Write-Host "✅ Schema copied to migrations" -ForegroundColor Green

# Start Supabase
Write-Host "Starting Supabase (this may take a few minutes)..." -ForegroundColor Yellow
supabase start

# Apply schema
Write-Host "Applying database schema..." -ForegroundColor Yellow
supabase db reset

Write-Host "🎉 Supabase setup complete!" -ForegroundColor Green
Write-Host "Dashboard: http://localhost:54323" -ForegroundColor Cyan
Write-Host "API: http://localhost:54321" -ForegroundColor Cyan

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
if (Test-Path "bot-anx/backend/requirements-supabase.txt") {
    pip install -r bot-anx/backend/requirements-supabase.txt
    Write-Host "✅ Python dependencies installed" -ForegroundColor Green
} else {
    pip install supabase postgrest-py realtime-py gotrue-py fastapi uvicorn python-dotenv
    Write-Host "✅ Core dependencies installed" -ForegroundColor Green
}

# Get connection details
Write-Host "Getting connection details..." -ForegroundColor Yellow
supabase status

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Copy the API URL and keys from above to bot-anx/backend/.env.supabase" -ForegroundColor White
Write-Host "2. Add your ClickUp, GitHub, and Vercel tokens to .env.supabase" -ForegroundColor White
Write-Host "3. Test connection: python test-supabase-connection.py" -ForegroundColor White
Write-Host "4. Start everything: start-superagent-supabase.bat" -ForegroundColor White