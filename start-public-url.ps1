# Turant public URL (local PC par server + tunnel)
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "PropertyBazaar server start thai rahyu che..." -ForegroundColor Cyan

$python = Join-Path $ProjectRoot "venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Host "venv nathi mali! Pehla: python -m venv venv" -ForegroundColor Red
    exit 1
}

Start-Process -FilePath $python -ArgumentList "manage.py","runserver","0.0.0.0:8000" -WorkingDirectory $ProjectRoot -WindowStyle Minimized

Start-Sleep -Seconds 4

Write-Host "Public link banavi rahyu che (30 second wait)..." -ForegroundColor Cyan

$npx = Get-Command npx -ErrorAction SilentlyContinue
if ($npx) {
    npx --yes localtunnel --port 8000
} else {
    Write-Host ""
    Write-Host "Node.js install karo: https://nodejs.org" -ForegroundColor Yellow
    Write-Host "Pachhi aa script fari run karo." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Local URL: http://127.0.0.1:8000/" -ForegroundColor Green
    Read-Host "Enter dabavo band karva"
}
