# 🚀 Ultimate Superagent - Windows Setup Guide

## Quick Start (5 Minutes)

### Option 1: Automated Setup (Recommended)
```powershell
# Run in PowerShell as Administrator
.\setup-supabase-simple.ps1
```

### Option 2: Manual Setup (If automated fails)

#### Step 1: Install Prerequisites
```powershell
# Check Node.js (required)
node --version
# If not installed: Download from https://nodejs.org

# Install Supabase CLI (choose one method)
# Method A: NPM (if working)
npm install -g supabase

# Method B: Winget (Windows 10/11)
winget install Supabase.cli

# Method C: Scoop (if you have Scoop)
scoop install supabase

# Method D: Direct download
# Go to: https://github.com/supabase/cli/releases
# Download supabase_windows_amd64.zip
# Extract and add to PATH
```

#### Step 2: Initialize Supabase
```powershell
# Initialize project
supabase init

# Start Supabase (this downloads Docker images)
supabase start
```

#### Step 3: Apply Database Schema
```powershell
# Copy schema to migrations
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
Copy-Item "supabase-schema.sql" "supabase/migrations/${timestamp}_initial_schema.sql"

# Apply schema
supabase db reset
```

#### Step 4: Install Python Dependencies
```powershell
# Install Supabase Python client
pip install supabase postgrest-py realtime-py gotrue-py

# Install other dependencies
pip install fastapi uvicorn python-dotenv requests
```

#### Step 5: Configure Environment
```powershell
# Get Supabase connection details
supabase status

# Copy the output values to bot-anx/backend/.env.supabase:
# - API URL -> SUPABASE_URL
# - anon key -> SUPABASE_ANON_KEY  
# - service_role key -> SUPABASE_SERVICE_ROLE_KEY
```

#### Step 6: Test Connection
```powershell
python test-supabase-connection.py
```

#### Step 7: Start Everything
```powershell
.\start-superagent-supabase.bat
```

## Troubleshooting Common Windows Issues

### Issue 1: "supabase command not found"
**Solutions:**
```powershell
# Check if installed
Get-Command supabase

# If not found, try:
# 1. Restart PowerShell/Command Prompt
# 2. Check PATH environment variable
# 3. Install using alternative method above
# 4. Use full path: C:\Users\[username]\AppData\Roaming\npm\supabase.cmd
```

### Issue 2: "Docker not available"
**Solutions:**
```powershell
# Option A: Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop

# Option B: Use Supabase Cloud (no Docker needed)
# 1. Go to https://supabase.com/dashboard
# 2. Create new project
# 3. Get URL and keys
# 4. Update .env.supabase with cloud values
```

### Issue 3: "Permission denied" or "Access denied"
**Solutions:**
```powershell
# Run PowerShell as Administrator
# Or change execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 4: "Port already in use"
**Solutions:**
```powershell
# Check what's using the ports
netstat -an | findstr :54321
netstat -an | findstr :54322
netstat -an | findstr :54323

# Stop conflicting services or change ports in supabase/config.toml
```

### Issue 5: "Python module not found"
**Solutions:**
```powershell
# Make sure you're in the right directory
cd bot-anx/backend

# Install in virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Or install globally
pip install supabase fastapi uvicorn python-dotenv
```

## Alternative: Cloud-Only Setup (No Docker)

If you can't get local Supabase working, use the cloud version:

### Step 1: Create Supabase Project
1. Go to https://supabase.com/dashboard
2. Click "New Project"
3. Choose organization and name
4. Wait for setup (2-3 minutes)

### Step 2: Get Connection Details
1. Go to Settings > API
2. Copy:
   - Project URL
   - anon/public key
   - service_role/secret key

### Step 3: Update Configuration
Edit `bot-anx/backend/.env.supabase`:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### Step 4: Apply Schema
1. Go to SQL Editor in Supabase dashboard
2. Copy contents of `supabase-schema.sql`
3. Paste and run

### Step 5: Test and Start
```powershell
python test-supabase-connection.py
.\start-superagent-supabase.bat
```

## What You Get After Setup

### 🎯 Core Capabilities
- **Ticket-Driven Development**: ClickUp tickets → Automated code
- **Real-time Monitoring**: Live progress updates
- **Quality Gates**: TDD, code review, security checks
- **Auto-Deployment**: GitHub → Vercel pipeline
- **High-Performance Workers**: Rust-based execution

### 🔧 Services Running
- **Supabase**: Database + Real-time + Dashboard
- **Bot-ANX**: FastAPI backend (port 8001)
- **Coordinator**: Rust coordination system (port 8002)
- **Webhook Handler**: GitHub/ClickUp webhooks (port 8003)

### 📊 Monitoring Dashboards
- **Supabase Dashboard**: http://localhost:54323
- **Bot-ANX API**: http://localhost:8001/docs
- **Real-time Events**: Live WebSocket updates

### 🚀 Workflow Example
1. Create ticket in ClickUp with acceptance criteria
2. Superagent generates implementation plan
3. AnesusBot workers execute code changes
4. Quality gates verify TDD compliance
5. Auto-deploy to Vercel with PR
6. Real-time progress tracking throughout

## Next Steps

1. **Add API Tokens**: Update `.env.supabase` with your actual tokens
2. **Test Integration**: Create a test ticket in ClickUp
3. **Monitor Progress**: Watch real-time updates in dashboard
4. **Scale Up**: Add more workers, enable production features

## Getting Help

### Check Logs
```powershell
# Supabase logs
supabase logs

# Bot-ANX logs (check the terminal window)
# Coordinator logs (check the terminal window)
```

### Verify Setup
```powershell
# Test each component
python test-supabase-connection.py
curl http://localhost:8001/health
curl http://localhost:8002/status
```

### Common Commands
```powershell
# Restart Supabase
supabase stop
supabase start

# Reset database
supabase db reset

# View status
supabase status

# Update schema
supabase db push
```

**Your Ultimate Superagent will be running at full capacity! 🎉**