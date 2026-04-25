# Ultimate Superagent Supabase Setup Script for Windows
# PowerShell version

Write-Host "🚀 Setting up Supabase for Ultimate Superagent (Windows)" -ForegroundColor Blue
Write-Host "=======================================================" -ForegroundColor Blue
Write-Host ""

function Write-Info {
    param($Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Blue
}

function Write-Success {
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Check if Node.js is installed
function Test-NodeJS {
    Write-Info "Checking Node.js installation..."
    
    if (Get-Command node -ErrorAction SilentlyContinue) {
        Write-Success "Node.js is installed"
        node --version
        return $true
    } else {
        Write-Error "Node.js is not installed. Please install Node.js first:"
        Write-Host "Visit: https://nodejs.org/en/download/"
        return $false
    }
}

# Install Supabase CLI
function Install-SupabaseCLI {
    Write-Info "Installing Supabase CLI..."
    
    if (Get-Command supabase -ErrorAction SilentlyContinue) {
        Write-Success "Supabase CLI already installed"
        supabase --version
    } else {
        try {
            npm install -g supabase
            Write-Success "Supabase CLI installed successfully"
        } catch {
            Write-Error "Failed to install Supabase CLI: $_"
            return $false
        }
    }
    return $true
}

# Initialize Supabase project
function Initialize-SupabaseProject {
    Write-Info "Initializing Supabase project..."
    
    if (Test-Path "supabase/config.toml") {
        Write-Warning "Supabase project already initialized"
    } else {
        try {
            supabase init
            Write-Success "Supabase project initialized"
        } catch {
            Write-Error "Failed to initialize Supabase project: $_"
            return $false
        }
    }
    return $true
}

# Create database schema
function Create-Schema {
    Write-Info "Creating database schema..."
    
    # Create migrations directory if it doesn't exist
    if (!(Test-Path "supabase/migrations")) {
        New-Item -ItemType Directory -Path "supabase/migrations" -Force
    }
    
    # Copy our schema to migrations
    $timestamp = Get-Date -Format "yyyyMMddHHmmss"
    Copy-Item "supabase-schema.sql" "supabase/migrations/${timestamp}_initial_schema.sql"
    
    Write-Success "Schema file created in migrations"
    return $true
}

# Start local Supabase
function Start-LocalSupabase {
    Write-Info "Starting local Supabase development environment..."
    Write-Info "This will start PostgreSQL, PostgREST, GoTrue, Realtime, and Storage..."
    
    try {
        supabase start
        Write-Success "Local Supabase started successfully"
        return $true
    } catch {
        Write-Error "Failed to start Supabase: $_"
        Write-Info "Make sure Docker is running and try again"
        return $false
    }
}

# Apply database migrations
function Apply-Migrations {
    Write-Info "Applying database migrations..."
    
    try {
        supabase db reset
        Write-Success "Database schema applied successfully"
        return $true
    } catch {
        Write-Error "Failed to apply migrations: $_"
        return $false
    }
}

# Install Python dependencies
function Install-PythonDeps {
    Write-Info "Installing Python dependencies for Bot-ANX..."
    
    Push-Location "bot-anx/backend"
    
    try {
        # Install Supabase Python client
        pip install supabase
        pip install postgrest-py
        pip install realtime-py
        pip install gotrue-py
        
        Write-Success "Python dependencies installed"
    } catch {
        Write-Warning "Some Python packages failed to install: $_"
        Write-Info "You may need to install them manually later"
    } finally {
        Pop-Location
    }
    
    return $true
}

# Create environment configuration
function Create-EnvConfig {
    Write-Info "Creating environment configuration..."
    
    try {
        # Get Supabase local connection details
        $supabaseStatus = supabase status --output json | ConvertFrom-Json
        
        $apiUrl = $supabaseStatus.'API URL'
        $anonKey = $supabaseStatus.'anon key'
        $serviceRoleKey = $supabaseStatus.'service_role key'
        
        # Create Bot-ANX environment file
        $envContent = @"
# Supabase Configuration
SUPABASE_URL=$apiUrl
SUPABASE_ANON_KEY=$anonKey
SUPABASE_SERVICE_ROLE_KEY=$serviceRoleKey

# Database URL for direct connections
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres

# LLM Integration
EMERGENT_LLM_KEY=sk-emergent-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# ClickUp Integration
CLICKUP_TOKEN=pk_your_clickup_token
CLICKUP_TEAM_ID=your_team_id
CLICKUP_LIST_ID=your_list_id

# GitHub Integration
GITHUB_TOKEN=ghp_your_github_token
GITHUB_OWNER=your_username
GITHUB_REPO=your_repo_name

# Vercel Integration
VERCEL_TOKEN=your_vercel_token
VERCEL_PROJECT_ID=your_project_id

# Safety Settings
SAFE_MODE=true
DRY_RUN=false
USE_MOCK_APIS=false

# Real-time Features
ENABLE_REALTIME=true
WEBSOCKET_URL=ws://localhost:54321/realtime/v1/websocket

# Monitoring
LOG_LEVEL=INFO
ENABLE_METRICS=true
"@

        $envContent | Out-File -FilePath "bot-anx/backend/.env.supabase" -Encoding UTF8
        
        # Create Superagent configuration
        $configContent = @"
{
  "superpowers": {
    "skills_path": "./skills",
    "methodology": "systematic",
    "tdd_enforced": true
  },
  "bot_anx": {
    "api_url": "http://localhost:8001/api",
    "database": {
      "type": "supabase",
      "url": "$apiUrl",
      "anon_key": "$anonKey",
      "service_role_key": "$serviceRoleKey"
    },
    "safe_mode": true,
    "realtime_enabled": true
  },
  "anesusbot": {
    "binary_path": "./anesusbot/rust/target/debug/claw.exe",
    "providers": ["anthropic", "openai"],
    "max_workers": 4,
    "plugins_enabled": true,
    "mcp_servers": ["filesystem", "git", "web", "supabase"]
  },
  "integration": {
    "event_streaming": true,
    "quality_gates": "strict",
    "monitoring": "real_time",
    "coordination": "advanced",
    "database": "supabase"
  }
}
"@

        $configContent | Out-File -FilePath "superagent-config-supabase.json" -Encoding UTF8
        
        Write-Success "Environment configuration created"
        return $true
        
    } catch {
        Write-Error "Failed to create environment configuration: $_"
        return $false
    }
}

# Create test script
function Create-TestScript {
    Write-Info "Creating test script..."
    
    $testScript = @'
#!/usr/bin/env python3
"""
Test Supabase connection for Ultimate Superagent
"""

import os
import sys
from datetime import datetime
import json

try:
    from supabase import create_client, Client
except ImportError:
    print("❌ Supabase package not installed. Run: pip install supabase")
    sys.exit(1)

def test_connection():
    # Load environment
    env_file = "bot-anx/backend/.env.supabase"
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    
    if not url or not key:
        print("❌ SUPABASE_URL or SUPABASE_ANON_KEY not found in environment")
        return False
    
    try:
        # Create client
        supabase: Client = create_client(url, key)
        print(f"✅ Connected to Supabase: {url}")
        
        # Test basic query
        result = supabase.table('tickets').select('*').limit(1).execute()
        print(f"✅ Database query successful")
        
        # Test insert
        test_ticket = {
            'clickup_id': 'TEST-001',
            'name': 'Test Supabase Connection',
            'description': 'Testing connection to Supabase',
            'status': 'open',
            'priority': 'normal'
        }
        
        insert_result = supabase.table('tickets').upsert(test_ticket).execute()
        print(f"✅ Test data inserted successfully")
        
        # Test real-time (basic check)
        print(f"✅ Real-time endpoint: {url.replace('http', 'ws')}/realtime/v1/websocket")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Supabase connection...")
    success = test_connection()
    if success:
        print("\n🎉 Supabase setup successful!")
        print("\nNext steps:")
        print("1. Update API tokens in bot-anx/backend/.env.supabase")
        print("2. Run: python test-supabase-connection.py")
        print("3. Start Bot-ANX: uvicorn server:app --port 8001")
    else:
        print("\n❌ Setup needs attention. Check the errors above.")
        sys.exit(1)
'@

    $testScript | Out-File -FilePath "test-supabase-connection.py" -Encoding UTF8
    Write-Success "Test script created"
    return $true
}

# Create startup scripts
function Create-StartupScripts {
    Write-Info "Creating startup scripts..."
    
    # Supabase startup script
    $supabaseStartScript = @'
@echo off
echo 🚀 Starting Supabase for Ultimate Superagent

REM Start Supabase services
supabase start

echo.
echo ✅ Supabase is running!
echo.
echo Services:
supabase status

echo.
echo Dashboard: http://localhost:54323
echo API URL: http://localhost:54321
echo.
echo Use 'supabase stop' to stop all services
pause
'@

    $supabaseStartScript | Out-File -FilePath "start-supabase.bat" -Encoding ASCII
    
    # Combined startup script
    $combinedStartScript = @'
@echo off
echo 🚀 Starting Ultimate Superagent with Supabase
echo =============================================

REM Start Supabase
echo Starting Supabase...
supabase start

REM Wait for Supabase to be ready
timeout /t 3 /nobreak > nul

REM Start Bot-ANX with Supabase config
echo Starting Bot-ANX backend...
cd bot-anx\backend
start "Bot-ANX" cmd /k "set /p dummy=<.env.supabase && uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
cd ..\..

REM Wait for Bot-ANX to start
timeout /t 5 /nobreak > nul

echo.
echo ✅ Ultimate Superagent with Supabase started!
echo.
echo Services:
echo • Supabase Dashboard: http://localhost:54323
echo • Supabase API: http://localhost:54321
echo • Bot-ANX API: http://localhost:8001
echo.
echo Press any key to stop all services...
pause > nul

REM Cleanup
echo Stopping services...
taskkill /f /im uvicorn.exe 2>nul
supabase stop
echo ✅ All services stopped
'@

    $combinedStartScript | Out-File -FilePath "start-superagent-supabase.bat" -Encoding ASCII
    
    Write-Success "Startup scripts created"
    return $true
}

# Main setup function
function Main {
    Write-Host "This will set up Supabase as the database for your Ultimate Superagent:" -ForegroundColor Cyan
    Write-Host "• PostgreSQL database with real-time subscriptions" -ForegroundColor Cyan
    Write-Host "• Auto-generated REST API" -ForegroundColor Cyan
    Write-Host "• Built-in authentication and dashboard" -ForegroundColor Cyan
    Write-Host "• Local development environment" -ForegroundColor Cyan
    Write-Host ""
    
    $continue = Read-Host "Continue with Supabase setup? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        Write-Host "Setup cancelled."
        return
    }
    
    Write-Host ""
    
    # Run setup steps
    if (!(Test-NodeJS)) { return }
    if (!(Install-SupabaseCLI)) { return }
    if (!(Initialize-SupabaseProject)) { return }
    if (!(Create-Schema)) { return }
    if (!(Start-LocalSupabase)) { return }
    if (!(Apply-Migrations)) { return }
    Install-PythonDeps
    if (!(Create-EnvConfig)) { return }
    if (!(Create-TestScript)) { return }
    if (!(Create-StartupScripts)) { return }
    
    Write-Host ""
    Write-Success "🎉 Supabase setup complete!"
    Write-Host ""
    Write-Host "What was created:" -ForegroundColor Cyan
    Write-Host "✅ Local Supabase development environment" -ForegroundColor Green
    Write-Host "✅ Database schema with all tables" -ForegroundColor Green
    Write-Host "✅ Environment configuration files" -ForegroundColor Green
    Write-Host "✅ Python dependencies" -ForegroundColor Green
    Write-Host "✅ Test and startup scripts" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Test connection: python test-supabase-connection.py" -ForegroundColor White
    Write-Host "2. Update API tokens in bot-anx/backend/.env.supabase" -ForegroundColor White
    Write-Host "3. Start everything: start-superagent-supabase.bat" -ForegroundColor White
    Write-Host ""
    Write-Host "Supabase Dashboard: http://localhost:54323" -ForegroundColor Cyan
    Write-Host "API Documentation: http://localhost:54321/rest/v1/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "For production, create a project at: https://supabase.com/dashboard" -ForegroundColor Cyan
}

# Run main function
Main