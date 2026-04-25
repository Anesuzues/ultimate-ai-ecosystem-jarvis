# JARVIS — Windows launcher (PowerShell variant)
$root     = (Resolve-Path "$PSScriptRoot\..").Path
$backend  = Join-Path $root "backend"
$frontend = Join-Path $root "frontend"
$mongoData = "C:\data\db"
if (-not (Test-Path $mongoData)) { New-Item -ItemType Directory -Path $mongoData -Force | Out-Null }

Write-Host "Starting MongoDB..." -ForegroundColor Cyan
Start-Process -FilePath "mongod" -ArgumentList "--dbpath",$mongoData,"--bind_ip_all" -WindowStyle Normal
Start-Sleep -Seconds 3

Write-Host "Starting backend..." -ForegroundColor Cyan
Start-Process -FilePath "cmd.exe" -ArgumentList @(
  "/k", "cd /d `"$backend`" && .venv\Scripts\activate && uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
) -WindowStyle Normal
Start-Sleep -Seconds 4

Write-Host "Starting frontend..." -ForegroundColor Cyan
Start-Process -FilePath "cmd.exe" -ArgumentList @(
  "/k", "cd /d `"$frontend`" && yarn start"
) -WindowStyle Normal

Write-Host ""
Write-Host "All three components launched." -ForegroundColor Green
Write-Host "Visit http://localhost:3000 in your browser."
