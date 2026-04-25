# JARVIS Windows Local Setup
# Run as Administrator: .\setup.ps1
$ErrorActionPreference = "Stop"

function Info($m)  { Write-Host "[*] $m" -ForegroundColor Cyan }
function Ok($m)    { Write-Host "[OK] $m" -ForegroundColor Green }
function Warn($m)  { Write-Host "[!] $m" -ForegroundColor Yellow }
function Die($m)   { Write-Host "[X] $m" -ForegroundColor Red; exit 1 }

# ---- elevation check
$cur = [Security.Principal.WindowsPrincipal]::new(
        [Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $cur.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Warn "Not running as Administrator. Some installs may fail."
}

# ---- repo paths
$root      = (Resolve-Path "$PSScriptRoot\..").Path
$backend   = Join-Path $root "backend"
$frontend  = Join-Path $root "frontend"

# ---- winget helper
function Ensure($id, $cmd) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        Ok "$cmd already installed"
        return
    }
    Info "installing $id via winget…"
    try {
        winget install --id $id --silent --accept-source-agreements --accept-package-agreements | Out-Null
    } catch {
        Warn "winget install $id failed — install manually if missing."
    }
}

Info "Checking prerequisites (Python, Node, MongoDB, Yarn, Ollama optional)"
Ensure "Python.Python.3.11"   "python"
Ensure "OpenJS.NodeJS.LTS"    "node"
Ensure "MongoDB.Server"        "mongod"
Ensure "Yarn.Yarn"             "yarn"
# Ollama is optional
Ensure "Ollama.Ollama"         "ollama"

# refresh PATH for this session
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
            [Environment]::GetEnvironmentVariable("Path", "User")

# ---- backend
Info "Creating Python venv + installing requirements"
Push-Location $backend
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
.\.venv\Scripts\python.exe -m pip install --upgrade pip | Out-Null
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install emergentintegrations `
    --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
Pop-Location
Ok "Backend deps installed"

# ---- frontend
Info "Installing frontend deps"
Push-Location $frontend
yarn install
Pop-Location
Ok "Frontend deps installed"

# ---- env files
$lanIp = (Get-NetIPAddress -AddressFamily IPv4 |
         Where-Object { $_.IPAddress -notmatch '^(127|169|0)\.' -and $_.PrefixOrigin -ne 'WellKnown' } |
         Select-Object -First 1).IPAddress
if (-not $lanIp) { $lanIp = "127.0.0.1" }
Info "Using LAN IP: $lanIp"

$backendEnv = Join-Path $backend ".env"
if (-not (Test-Path $backendEnv)) {
    @"
MONGO_URL=mongodb://localhost:27017
DB_NAME=jarvis_db
EMERGENT_LLM_KEY=
LLM_PROVIDER=emergent
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
CORS_ORIGINS=*
"@ | Set-Content $backendEnv -Encoding UTF8
    Ok "Wrote $backendEnv (ADD YOUR EMERGENT_LLM_KEY!)"
} else {
    Ok "$backendEnv already exists — leaving as-is"
}

$frontendEnv = Join-Path $frontend ".env"
@"
REACT_APP_BACKEND_URL=http://$lanIp`:8001
WDS_SOCKET_PORT=0
HOST=0.0.0.0
PORT=3000
DANGEROUSLY_DISABLE_HOST_CHECK=true
"@ | Set-Content $frontendEnv -Encoding UTF8
Ok "Wrote $frontendEnv pointing to http://$lanIp`:8001"

# ---- MongoDB data dir
$mongoData = "C:\data\db"
if (-not (Test-Path $mongoData)) {
    New-Item -ItemType Directory -Path $mongoData -Force | Out-Null
    Ok "Created $mongoData"
}

# ---- firewall rules
Info "Adding firewall rules for ports 3000, 8001"
foreach ($p in 3000, 8001) {
    $name = "JARVIS-$p"
    if (-not (Get-NetFirewallRule -Name $name -ErrorAction SilentlyContinue)) {
        try {
            New-NetFirewallRule -Name $name -DisplayName "JARVIS port $p" `
                -Protocol TCP -LocalPort $p -Action Allow -Direction Inbound | Out-Null
            Ok "Firewall: opened port $p"
        } catch { Warn "Firewall: couldn't add rule for $p — run as admin to enable LAN access" }
    }
}

Write-Host ""
Ok "Setup complete!"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Edit $backendEnv and set EMERGENT_LLM_KEY  (or leave blank if using only Ollama)"
Write-Host "  2. Double-click  windows-local\start.bat   to launch everything"
Write-Host "  3. Open http://$lanIp`:3000  on this PC, or from your phone on the same Wi-Fi"
Write-Host ""
