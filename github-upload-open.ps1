# GitHub upload mate browser links khole
Write-Host "GitHub par repo banavo ane files upload karo..." -ForegroundColor Cyan
Write-Host ""
Write-Host "UPLOAD NATHI karvi: venv, .env, db.sqlite3, media, staticfiles" -ForegroundColor Yellow
Write-Host ""

$folder = $PSScriptRoot
Start-Process "https://github.com/new"
Start-Sleep -Seconds 2
explorer.exe $folder

Write-Host "Folder Explorer ma khuli gayu — files GitHub page par drag karo." -ForegroundColor Green
Write-Host "Guide: GITHUB_UPLOAD.md" -ForegroundColor Green
Read-Host "Done thay to Enter dabavo"
